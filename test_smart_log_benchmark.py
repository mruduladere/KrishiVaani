import copy
from app import FARMERS_DB, LIVESTOCK_DB, EXPENSES_DB, MARKETPLACE_DB, TASKS_DB, app
from smart_dispatcher import extract_and_dispatch

def test_all():
    print("==================================================")
    print("STARTING SMART LOG 6 BENCHMARK VERIFICATION TESTS")
    print("==================================================")

    farmer = FARMERS_DB["9822012345"]
    in_memory_dbs = {
        "livestock": copy.deepcopy(LIVESTOCK_DB),
        "expenses": copy.deepcopy(EXPENSES_DB),
        "marketplace": copy.deepcopy(MARKETPLACE_DB),
        "tasks": copy.deepcopy(TASKS_DB)
    }

    # ----------------------------------------------------
    # Benchmark 1: "I bought a cow named Gauri for ₹25,000."
    # ----------------------------------------------------
    print("\n--- Test 1: 'I bought a cow named Gauri for ₹25,000.' ---")
    prev_livestock_count = len(in_memory_dbs["livestock"])
    prev_expenses_count = len(in_memory_dbs["expenses"])
    res1 = extract_and_dispatch("I bought a cow named Gauri for ₹25,000.", farmer, in_memory_dbs, "en")
    
    assert res1["success"] is True, "Test 1 failed: extract_and_dispatch not successful"
    assert len(in_memory_dbs["livestock"]) == prev_livestock_count + 1, "Test 1 failed: livestock not added"
    assert len(in_memory_dbs["expenses"]) == prev_expenses_count + 1, "Test 1 failed: expense not added"
    
    new_animal = in_memory_dbs["livestock"][0]
    new_expense = in_memory_dbs["expenses"][0]
    
    assert new_animal["name"]["en"] == "Gauri", f"Test 1 failed: name is {new_animal['name']}"
    assert new_animal["registration_status"] == "Registration pending", f"Test 1 failed: status is {new_animal['registration_status']}"
    assert "PENDING" in new_animal["tag_id"], f"Test 1 failed: tag_id is {new_animal['tag_id']}"
    assert new_animal["purchase_price"] == 25000.0, f"Test 1 failed: price is {new_animal['purchase_price']}"
    assert new_animal["age_years"] == 0.0, f"Test 1 failed: fabricated age {new_animal['age_years']}"
    assert len(new_animal["vaccination_history"]) == 0, f"Test 1 failed: fabricated vaccine {new_animal['vaccination_history']}"
    
    assert new_expense["amount"] == 25000.0, f"Test 1 failed: expense amount is {new_expense['amount']}"
    assert new_expense["category"]["en"] == "Livestock Purchase", f"Test 1 failed: category is {new_expense['category']}"
    print("PASS: Multi-action executed cleanly (Expense of ₹25,000 logged + Cattle 'Gauri' initiated with Registration Pending, no fabricated age/vaccine).")

    # Deduplication test: Resubmitting exact same statement
    res1_dup = extract_and_dispatch("I bought a cow named Gauri for ₹25,000.", farmer, in_memory_dbs, "en")
    assert len(in_memory_dbs["livestock"]) == prev_livestock_count + 1, "Deduplication failed: Duplicate livestock created!"
    assert len(in_memory_dbs["expenses"]) == prev_expenses_count + 1, "Deduplication failed: Duplicate expense created!"
    print("PASS: Resubmission de-duplication confirmed (no duplicate livestock or expense created).")

    # ----------------------------------------------------
    # Benchmark 2: "I completed Gauri's vaccination today."
    # ----------------------------------------------------
    print("\n--- Test 2: 'I completed Gauri's vaccination today.' ---")
    livestock_count_before = len(in_memory_dbs["livestock"])
    expenses_count_before = len(in_memory_dbs["expenses"])
    
    res2 = extract_and_dispatch("I completed Gauri's vaccination today.", farmer, in_memory_dbs, "en")
    assert res2["success"] is True, "Test 2 failed"
    assert len(in_memory_dbs["livestock"]) == livestock_count_before, "Test 2 failed: created new animal instead of updating existing!"
    assert len(in_memory_dbs["expenses"]) == expenses_count_before, "Test 2 failed: created expense for vaccination completion!"
    
    # Check Gauri record
    gauri = next(a for a in in_memory_dbs["livestock"] if (a["name"].get("en") if isinstance(a["name"], dict) else a["name"]) == "Gauri")
    assert len(gauri["vaccination_history"]) > 0, "Test 2 failed: no vaccination history on Gauri"
    fmd = gauri["vaccination_history"][0]
    assert fmd["status"] == "Up-to-Date", f"Test 2 failed: status is {fmd['status']}"
    print(f"PASS: Updated existing Gauri ({gauri['tag_id']}) vaccination status to Up-to-Date. Zero duplicate cows or fake expenses.")

    # ----------------------------------------------------
    # Benchmark 3: "My ten cows produced 65 litres of milk today."
    # ----------------------------------------------------
    print("\n--- Test 3: 'My ten cows produced 65 litres of milk today.' ---")
    livestock_count_before = len(in_memory_dbs["livestock"])
    expenses_count_before = len(in_memory_dbs["expenses"])
    
    res3 = extract_and_dispatch("My ten cows produced 65 litres of milk today.", farmer, in_memory_dbs, "en")
    assert res3["success"] is True, "Test 3 failed"
    assert len(in_memory_dbs["livestock"]) == livestock_count_before, "Test 3 failed: created animal for milk production!"
    assert len(in_memory_dbs["expenses"]) == expenses_count_before, "Test 3 failed: created expense for milk production!"
    assert farmer["livestock_summary"]["daily_milk_litres"] == 65.0, f"Test 3 failed: daily_milk_litres is {farmer['livestock_summary']['daily_milk_litres']}"
    print(f"PASS: Milk yield updated to {farmer['livestock_summary']['daily_milk_litres']} L on farmer dashboard. No fake expense or cow added.")

    # ----------------------------------------------------
    # Benchmark 4: "I purchased fertiliser for ₹1,200."
    # ----------------------------------------------------
    print("\n--- Test 4: 'I purchased fertiliser for ₹1,200.' ---")
    expenses_count_before = len(in_memory_dbs["expenses"])
    res4 = extract_and_dispatch("I purchased fertiliser for ₹1,200.", farmer, in_memory_dbs, "en")
    assert res4["success"] is True, "Test 4 failed"
    assert len(in_memory_dbs["expenses"]) == expenses_count_before + 1, "Test 4 failed: expense not added"
    exp4 = in_memory_dbs["expenses"][0]
    assert exp4["amount"] == 1200.0, f"Test 4 failed: amount is {exp4['amount']}"
    assert exp4["category"]["en"] == "Fertilizers & Nutrients", f"Test 4 failed: category is {exp4['category']}"
    print(f"PASS: Logged expense of ₹{exp4['amount']} under {exp4['category']['en']}.")

    # ----------------------------------------------------
    # Benchmark 5: "I sold onions for ₹8,000."
    # ----------------------------------------------------
    print("\n--- Test 5: 'I sold onions for ₹8,000.' ---")
    expenses_count_before = len(in_memory_dbs["expenses"])
    res5 = extract_and_dispatch("I sold onions for ₹8,000.", farmer, in_memory_dbs, "en")
    assert res5["success"] is True, "Test 5 failed"
    assert len(in_memory_dbs["expenses"]) == expenses_count_before + 1, "Test 5 failed: income not added to expenses tracker"
    inc5 = in_memory_dbs["expenses"][0]
    assert inc5["amount"] == 8000.0, f"Test 5 failed: amount is {inc5['amount']}"
    assert inc5["crop"]["en"] == "Onion", f"Test 5 failed: crop is {inc5['crop']}"
    assert inc5["category"]["en"] == "Produce Sales & Income", f"Test 5 failed: category is {inc5['category']}"
    print(f"PASS: Farm income of ₹{inc5['amount']} from {inc5['crop']['en']} recorded under {inc5['category']['en']}.")

    # ----------------------------------------------------
    # Benchmark 6: "I bought a cow named Gauri" (No price, no reg number)
    # ----------------------------------------------------
    print("\n--- Test 6: 'I bought a cow named Gauri' (No price, no reg) ---")
    # Using fresh DB to test standalone addition without prior Gauri pending
    fresh_dbs = {
        "livestock": [copy.deepcopy(LIVESTOCK_DB[1])], # only Lakshmi
        "expenses": [],
        "marketplace": [],
        "tasks": []
    }
    res6 = extract_and_dispatch("I bought a cow named Gauri", farmer, fresh_dbs, "en")
    assert res6["success"] is True, "Test 6 failed"
    assert len(fresh_dbs["livestock"]) == 2, "Test 6 failed: cattle not added"
    assert len(fresh_dbs["expenses"]) == 0, "Test 6 failed: invented fake expense when no price was given!"
    
    animal6 = fresh_dbs["livestock"][0]
    assert animal6["name"]["en"] == "Gauri", f"Test 6 failed: name is {animal6['name']}"
    assert animal6["registration_status"] == "Registration pending", f"Test 6 failed: status is {animal6['registration_status']}"
    assert animal6["purchase_price"] is None, f"Test 6 failed: invented purchase price {animal6['purchase_price']}"
    assert animal6["age_years"] == 0.0, f"Test 6 failed: invented age {animal6['age_years']}"
    assert len(animal6["vaccination_history"]) == 0, f"Test 6 failed: invented vaccine {animal6['vaccination_history']}"
    assert res6["has_pending_cattle"] is True, "Test 6 failed: has_pending_cattle not set"
    assert len(res6["notifications"]) > 0, "Test 6 failed: no registration pending notification"
    print(f"PASS: Animal 'Gauri' added with Registration Pending. ZERO fake expense created, ZERO fabricated age/vaccine. Official tag reminder active.")

    # ----------------------------------------------------
    # Web Client Route Test (/smart-log and /smart-log/submit)
    # ----------------------------------------------------
    print("\n--- Test 7: Web Endpoint Verification ---")
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["is_authenticated"] = True
            sess["phone"] = "9822012345"
            sess["lang"] = "en"
            sess["farmer_profile"] = copy.deepcopy(farmer)

        # GET /smart-log
        resp_get = client.get("/smart-log")
        assert resp_get.status_code == 200, f"GET /smart-log returned {resp_get.status_code}"

        # POST /smart-log/submit
        resp_post = client.post("/smart-log/submit", data={"raw_text": "I purchased fertiliser for ₹1,200."}, follow_redirects=True)
        assert resp_post.status_code == 200, f"POST /smart-log/submit returned {resp_post.status_code}"
        assert b"Fertilizers & Nutrients" in resp_post.data or b"Allocated" in resp_post.data
        print("PASS: /smart-log and /smart-log/submit returned HTTP 200 and rendered allocation cards.")

    print("\n==================================================")
    print("ALL 6 BENCHMARK TESTS & DEDUPLICATION PASSED 100%!")
    print("==================================================")

if __name__ == "__main__":
    test_all()
