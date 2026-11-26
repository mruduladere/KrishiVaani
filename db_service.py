"""
db_service.py - Supabase Persistence Layer for KrishiVaani
Provides server-side CRUD operations scoped by farmer_phone with graceful
in-memory fallback when Supabase credentials are not configured.
"""

import os
import copy
import logging
from pathlib import Path
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

from sample_data import (
    SAMPLE_FARMER,
    SAMPLE_REGISTERED_FARMERS,
    SAMPLE_SERVICES,
    SAMPLE_CROP_TASKS,
    SAMPLE_LIVESTOCK,
    SAMPLE_MARKETPLACE,
    SAMPLE_EXPENSES,
)

env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=False)
else:
    load_dotenv(override=False)

logger = logging.getLogger("krishivaani.db")

_supabase_client = None
_demo_seeded = False


def get_supabase_client():
    """Returns a cached Supabase client if SUPABASE_URL and key are configured, else None."""
    global _supabase_client
    url = (
        os.environ.get("SUPABASE_URL", "").strip()
        or os.environ.get("NEXT_PUBLIC_SUPABASE_URL", "").strip()
    )
    key = (
        os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
        or os.environ.get("SUPABASE_KEY", "").strip()
    )
    if not url or not key:
        return None

    if _supabase_client is None:
        try:
            from supabase import create_client
            _supabase_client = create_client(url, key)
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            return None
    return _supabase_client


def is_supabase_configured() -> bool:
    """True when both SUPABASE_URL and a service/API key are present."""
    return get_supabase_client() is not None


def _normalize_phone(phone_str: str) -> str:
    if not phone_str:
        return ""
    cleaned = "".join(c for c in str(phone_str) if c.isdigit())
    if len(cleaned) > 10 and cleaned.startswith("91"):
        cleaned = cleaned[2:]
    return cleaned


def _strip_secret_fields(farmer_dict: dict) -> dict:
    """Removes pin_hash before storing farmer profile in session cookies."""
    if not farmer_dict:
        return {}
    cleaned = copy.deepcopy(farmer_dict)
    cleaned.pop("pin_hash", None)
    cleaned.pop("pin", None)
    return cleaned


def _row_to_farmer(row: dict) -> dict:
    return {
        "name": row.get("name"),
        "phone": row.get("phone"),
        "email": row.get("email"),
        "village": row.get("village"),
        "taluka": row.get("taluka"),
        "district": row.get("district"),
        "state": row.get("state"),
        "pincode": row.get("pincode"),
        "land_size_acres": float(row.get("land_size_acres") or 0),
        "soil_type": row.get("soil_type"),
        "irrigation_type": row.get("irrigation_type"),
        "primary_language": row.get("primary_language"),
        "crops_grown": row.get("crops_grown") or [],
        "livestock_summary": row.get("livestock_summary") or {},
    }


def ensure_demo_seeded() -> None:
    """Idempotently seeds the demo farmer (9822012345) and sample data if absent in Supabase."""
    global _demo_seeded
    if _demo_seeded:
        return
    client = get_supabase_client()
    if not client:
        return

    try:
        existing = client.table("farmers").select("phone").eq("phone", "9822012345").execute()
        if existing.data:
            _demo_seeded = True
            return

        demo_row = {
            "phone": "9822012345",
            "pin_hash": generate_password_hash(SAMPLE_FARMER.get("pin", "1234")),
            "name": SAMPLE_FARMER["name"],
            "email": SAMPLE_FARMER.get("email"),
            "village": SAMPLE_FARMER.get("village"),
            "taluka": SAMPLE_FARMER.get("taluka"),
            "district": SAMPLE_FARMER.get("district"),
            "state": SAMPLE_FARMER.get("state"),
            "pincode": SAMPLE_FARMER.get("pincode"),
            "land_size_acres": SAMPLE_FARMER.get("land_size_acres", 4.5),
            "soil_type": SAMPLE_FARMER.get("soil_type"),
            "irrigation_type": SAMPLE_FARMER.get("irrigation_type"),
            "primary_language": SAMPLE_FARMER.get("primary_language"),
            "crops_grown": SAMPLE_FARMER.get("crops_grown", []),
            "livestock_summary": SAMPLE_FARMER.get("livestock_summary", {}),
        }
        client.table("farmers").upsert(demo_row, on_conflict="phone").execute()

        # Seed tasks, livestock, expenses, marketplace, services
        tasks_rows = [{**t, "farmer_phone": "9822012345"} for t in SAMPLE_CROP_TASKS]
        if tasks_rows:
            client.table("crop_tasks").upsert(tasks_rows, on_conflict="id").execute()

        ls_rows = [{**a, "farmer_phone": "9822012345"} for a in SAMPLE_LIVESTOCK]
        if ls_rows:
            client.table("livestock").upsert(ls_rows, on_conflict="tag_id").execute()

        exp_rows = [{**e, "farmer_phone": "9822012345", "entry_type": e.get("entry_type", "expense")} for e in SAMPLE_EXPENSES]
        if exp_rows:
            client.table("expenses").upsert(exp_rows, on_conflict="id").execute()

        mkt_rows = [{**m, "farmer_phone": "9822012345"} for m in SAMPLE_MARKETPLACE]
        if mkt_rows:
            client.table("marketplace_listings").upsert(mkt_rows, on_conflict="id").execute()

        srv_rows = [{**s, "added_by_phone": "9822012345"} for s in SAMPLE_SERVICES]
        if srv_rows:
            client.table("nearby_services").upsert(srv_rows, on_conflict="id").execute()

        _demo_seeded = True
    except Exception as e:
        logger.warning(f"Demo seed skipped or failed: {e}")


# ---------------------------------------------------------------------------
# FARMERS (AUTH & PROFILE)
# ---------------------------------------------------------------------------

def authenticate_farmer(phone: str, pin: str, fallback_db: dict) -> tuple[dict | None, str | None]:
    """Validates phone + PIN against Supabase (or fallback_db if Supabase is unconfigured)."""
    cleaned_phone = _normalize_phone(phone)
    client = get_supabase_client()
    if client:
        if cleaned_phone == "9822012345":
            ensure_demo_seeded()
        try:
            res = client.table("farmers").select("*").eq("phone", cleaned_phone).execute()
            if not res.data:
                return None, None
            row = res.data[0]
            stored_hash = row.get("pin_hash", "")
            if stored_hash and check_password_hash(stored_hash, pin):
                return _row_to_farmer(row), None
            return None, None
        except Exception as e:
            logger.error(f"Supabase authenticate_farmer error: {e}")
            return None, str(e)

    # Fallback: in-memory dictionary
    for reg_phone, profile in fallback_db.items():
        if _normalize_phone(reg_phone) == cleaned_phone and profile.get("pin") == pin:
            return copy.deepcopy(profile), None
    return None, None


def get_farmer_by_phone(phone: str, fallback_db: dict) -> dict | None:
    cleaned_phone = _normalize_phone(phone)
    client = get_supabase_client()
    if client:
        if cleaned_phone == "9822012345":
            ensure_demo_seeded()
        try:
            res = client.table("farmers").select("*").eq("phone", cleaned_phone).execute()
            if res.data:
                return _row_to_farmer(res.data[0])
        except Exception as e:
            logger.warning(f"Supabase get_farmer_by_phone error: {e}")

    for reg_phone, profile in fallback_db.items():
        if _normalize_phone(reg_phone) == cleaned_phone:
            return copy.deepcopy(profile)
    return None


def register_farmer(farmer_data: dict, pin: str, fallback_db: dict) -> tuple[bool, str | None]:
    cleaned_phone = _normalize_phone(farmer_data.get("phone", ""))
    client = get_supabase_client()
    if client:
        try:
            existing = client.table("farmers").select("phone").eq("phone", cleaned_phone).execute()
            if existing.data:
                return False, "A farmer account with this mobile number already exists."
            row = {
                "phone": cleaned_phone,
                "pin_hash": generate_password_hash(pin),
                "name": farmer_data.get("name"),
                "email": farmer_data.get("email"),
                "village": farmer_data.get("village"),
                "taluka": farmer_data.get("taluka"),
                "district": farmer_data.get("district"),
                "state": farmer_data.get("state", "Maharashtra"),
                "pincode": farmer_data.get("pincode", "422001"),
                "land_size_acres": float(farmer_data.get("land_size_acres") or 0),
                "soil_type": farmer_data.get("soil_type"),
                "irrigation_type": farmer_data.get("irrigation_type"),
                "primary_language": farmer_data.get("primary_language"),
                "crops_grown": farmer_data.get("crops_grown", []),
                "livestock_summary": farmer_data.get("livestock_summary", {}),
            }
            client.table("farmers").insert(row).execute()
            return True, None
        except Exception as e:
            logger.error(f"Supabase register_farmer error: {e}")
            return False, str(e)

    fallback_db[cleaned_phone] = copy.deepcopy(farmer_data)
    return True, None


def update_farmer_profile(phone: str, updates: dict, fallback_db: dict) -> tuple[bool, str | None]:
    cleaned_phone = _normalize_phone(phone)
    client = get_supabase_client()
    if client:
        try:
            payload = {k: v for k, v in updates.items() if k not in ("phone", "pin", "pin_hash")}
            client.table("farmers").update(payload).eq("phone", cleaned_phone).execute()
            return True, None
        except Exception as e:
            logger.error(f"Supabase update_farmer_profile error: {e}")
            return False, str(e)

    if cleaned_phone in fallback_db:
        fallback_db[cleaned_phone].update(updates)
    return True, None


# ---------------------------------------------------------------------------
# CROP TASKS
# ---------------------------------------------------------------------------

def list_crop_tasks(phone: str, fallback_list: list) -> list:
    cleaned_phone = _normalize_phone(phone)
    client = get_supabase_client()
    if client:
        if cleaned_phone == "9822012345":
            ensure_demo_seeded()
        try:
            res = (
                client.table("crop_tasks")
                .select("*")
                .eq("farmer_phone", cleaned_phone)
                .order("created_at", desc=True)
                .execute()
            )
            return res.data or []
        except Exception as e:
            logger.warning(f"Supabase list_crop_tasks error, falling back: {e}")
    return fallback_list


def add_crop_task(phone: str, task: dict, fallback_list: list) -> tuple[bool, str | None]:
    cleaned_phone = _normalize_phone(phone)
    client = get_supabase_client()
    if client:
        try:
            row = {
                "id": task["id"],
                "farmer_phone": cleaned_phone,
                "crop": task["crop"],
                "title": task["title"],
                "stage": task.get("stage"),
                "due_date": task.get("due_date"),
                "priority": task.get("priority"),
                "status": bool(task.get("status", False)),
            }
            client.table("crop_tasks").insert(row).execute()
            return True, None
        except Exception as e:
            logger.error(f"Supabase add_crop_task error: {e}")
            return False, str(e)

    fallback_list.insert(0, task)
    return True, None


def toggle_crop_task(phone: str, task_id: str, new_status: bool, fallback_list: list) -> tuple[bool, str | None]:
    cleaned_phone = _normalize_phone(phone)
    client = get_supabase_client()
    if client:
        try:
            client.table("crop_tasks").update({"status": new_status}).eq("id", task_id).eq("farmer_phone", cleaned_phone).execute()
            return True, None
        except Exception as e:
            logger.error(f"Supabase toggle_crop_task error: {e}")
            return False, str(e)

    for task in fallback_list:
        if task.get("id") == task_id:
            task["status"] = new_status
            break
    return True, None


# ---------------------------------------------------------------------------
# LIVESTOCK
# ---------------------------------------------------------------------------

def list_livestock(phone: str, fallback_list: list) -> list:
    cleaned_phone = _normalize_phone(phone)
    client = get_supabase_client()
    if client:
        if cleaned_phone == "9822012345":
            ensure_demo_seeded()
        try:
            res = (
                client.table("livestock")
                .select("*")
                .eq("farmer_phone", cleaned_phone)
                .order("created_at", desc=True)
                .execute()
            )
            return res.data or []
        except Exception as e:
            logger.warning(f"Supabase list_livestock error, falling back: {e}")
    return fallback_list


def add_livestock(phone: str, animal: dict, fallback_list: list) -> tuple[bool, str | None]:
    cleaned_phone = _normalize_phone(phone)
    client = get_supabase_client()
    if client:
        try:
            row = {
                "tag_id": animal["tag_id"],
                "farmer_phone": cleaned_phone,
                "name": animal["name"],
                "type": animal["type"],
                "breed": animal.get("breed"),
                "age_years": animal.get("age_years"),
                "daily_milk_yield_litres": float(animal.get("daily_milk_yield_litres") or 0),
                "health_status": animal.get("health_status"),
                "vaccination_history": animal.get("vaccination_history", []),
                "production_logs": animal.get("production_logs", []),
                "purchase_date": animal.get("purchase_date"),
                "purchase_price": animal.get("purchase_price"),
                "pending_completion": bool(animal.get("pending_completion", False)),
            }
            client.table("livestock").insert(row).execute()
            return True, None
        except Exception as e:
            logger.error(f"Supabase add_livestock error: {e}")
            return False, str(e)

    fallback_list.append(animal)
    return True, None


def update_livestock(phone: str, tag_id: str, updates: dict, fallback_list: list) -> tuple[bool, str | None]:
    cleaned_phone = _normalize_phone(phone)
    client = get_supabase_client()
    if client:
        try:
            allowed = {
                k: v for k, v in updates.items()
                if k in (
                    "tag_id", "name", "type", "breed", "age_years",
                    "daily_milk_yield_litres", "health_status",
                    "vaccination_history", "production_logs",
                    "purchase_date", "purchase_price", "pending_completion"
                )
            }
            client.table("livestock").update(allowed).eq("tag_id", tag_id).eq("farmer_phone", cleaned_phone).execute()
            return True, None
        except Exception as e:
            logger.error(f"Supabase update_livestock error: {e}")
            return False, str(e)

    for animal in fallback_list:
        if animal.get("tag_id") == tag_id:
            animal.update(updates)
            break
    return True, None


# ---------------------------------------------------------------------------
# EXPENSES & INCOME
# ---------------------------------------------------------------------------

def list_expenses(phone: str, fallback_list: list) -> list:
    cleaned_phone = _normalize_phone(phone)
    client = get_supabase_client()
    if client:
        if cleaned_phone == "9822012345":
            ensure_demo_seeded()
        try:
            res = (
                client.table("expenses")
                .select("*")
                .eq("farmer_phone", cleaned_phone)
                .order("date", desc=True)
                .execute()
            )
            return res.data or []
        except Exception as e:
            logger.warning(f"Supabase list_expenses error, falling back: {e}")
    return fallback_list


def add_expense_record(phone: str, expense: dict, fallback_list: list) -> tuple[bool, str | None]:
    cleaned_phone = _normalize_phone(phone)
    client = get_supabase_client()
    if client:
        try:
            row = {
                "id": expense["id"],
                "farmer_phone": cleaned_phone,
                "date": str(expense["date"]),
                "month": expense.get("month"),
                "season": expense.get("season"),
                "crop": expense.get("crop"),
                "category": expense["category"],
                "description": expense.get("description"),
                "amount": float(expense.get("amount") or 0),
                "payment_mode": expense.get("payment_mode"),
                "entry_type": expense.get("entry_type", "expense"),
            }
            client.table("expenses").insert(row).execute()
            return True, None
        except Exception as e:
            logger.error(f"Supabase add_expense_record error: {e}")
            return False, str(e)

    fallback_list.insert(0, expense)
    return True, None


def delete_expense_record(phone: str, expense_id: str, fallback_list: list) -> tuple[bool, str | None]:
    cleaned_phone = _normalize_phone(phone)
    client = get_supabase_client()
    if client:
        try:
            client.table("expenses").delete().eq("id", expense_id).eq("farmer_phone", cleaned_phone).execute()
            return True, None
        except Exception as e:
            logger.error(f"Supabase delete_expense_record error: {e}")
            return False, str(e)

    fallback_list[:] = [e for e in fallback_list if e.get("id") != expense_id]
    return True, None


# ---------------------------------------------------------------------------
# MARKETPLACE LISTINGS (SHARED READ, OWNER SCOPED WRITE)
# ---------------------------------------------------------------------------

def list_marketplace(fallback_list: list) -> list:
    client = get_supabase_client()
    if client:
        ensure_demo_seeded()
        try:
            res = (
                client.table("marketplace_listings")
                .select("*")
                .order("created_at", desc=True)
                .execute()
            )
            return res.data or []
        except Exception as e:
            logger.warning(f"Supabase list_marketplace error, falling back: {e}")
    return fallback_list


def add_marketplace_record(phone: str, listing: dict, fallback_list: list) -> tuple[bool, str | None]:
    cleaned_phone = _normalize_phone(phone)
    client = get_supabase_client()
    if client:
        try:
            row = {
                "id": listing["id"],
                "farmer_phone": cleaned_phone or None,
                "crop_name": listing["crop_name"],
                "category": listing.get("category"),
                "variety": listing.get("variety"),
                "quality_grade": listing.get("quality_grade"),
                "quantity_quintals": float(listing.get("quantity_quintals") or 0),
                "expected_price_per_quintal": float(listing.get("expected_price_per_quintal") or 0),
                "seller_name": listing.get("seller_name"),
                "seller_phone": listing.get("seller_phone"),
                "village": listing.get("village"),
                "taluka": listing.get("taluka"),
                "district": listing.get("district"),
                "location": listing.get("location"),
                "harvest_date": listing.get("harvest_date"),
                "status": listing.get("status"),
                "notes": listing.get("notes"),
            }
            client.table("marketplace_listings").insert(row).execute()
            return True, None
        except Exception as e:
            logger.error(f"Supabase add_marketplace_record error: {e}")
            return False, str(e)

    fallback_list.insert(0, listing)
    return True, None


# ---------------------------------------------------------------------------
# NEARBY SERVICES (SHARED REGIONAL DIRECTORY)
# ---------------------------------------------------------------------------

def list_nearby_services(fallback_list: list) -> list:
    client = get_supabase_client()
    if client:
        ensure_demo_seeded()
        try:
            res = (
                client.table("nearby_services")
                .select("*")
                .order("created_at", desc=False)
                .execute()
            )
            return res.data or []
        except Exception as e:
            logger.warning(f"Supabase list_nearby_services error, falling back: {e}")
    return fallback_list


def add_nearby_service_record(phone: str, service: dict, fallback_list: list) -> tuple[bool, str | None]:
    cleaned_phone = _normalize_phone(phone)
    client = get_supabase_client()
    if client:
        try:
            row = {
                "id": service["id"],
                "added_by_phone": cleaned_phone or None,
                "name": service["name"],
                "category": service["category"],
                "taluka": service.get("taluka"),
                "district": service.get("district"),
                "location": service.get("location"),
                "phone": service.get("phone"),
                "timings": service.get("timings"),
                "speciality": service.get("speciality"),
                "rating": float(service.get("rating") or 4.5),
                "verified": bool(service.get("verified", True)),
            }
            client.table("nearby_services").insert(row).execute()
            return True, None
        except Exception as e:
            logger.error(f"Supabase add_nearby_service_record error: {e}")
            return False, str(e)

    fallback_list.append(service)
    return True, None
