-- KrishiVaani Initial Supabase PostgreSQL Schema
-- Preserves bilingual JSONB structure ({"en": ..., "mr": ...}) used by Flask & Jinja2 templates.

-- 1. Farmers Profile & Authentication Table
CREATE TABLE IF NOT EXISTS public.farmers (
    phone TEXT PRIMARY KEY, -- Normalized 10-digit mobile number (e.g., '9822012345')
    pin_hash TEXT NOT NULL, -- Werkzeug password hash of 4-digit PIN
    name JSONB NOT NULL,
    email TEXT,
    village JSONB,
    taluka JSONB,
    district JSONB,
    state JSONB DEFAULT '{"en": "Maharashtra", "mr": "महाराष्ट्र"}'::jsonb,
    pincode TEXT,
    land_size_acres NUMERIC(10, 2) DEFAULT 0,
    soil_type JSONB,
    irrigation_type JSONB,
    primary_language JSONB,
    crops_grown JSONB DEFAULT '[]'::jsonb,
    livestock_summary JSONB DEFAULT '{"gir_cows": 0, "murrah_buffaloes": 0, "goats": 0, "total_animals": 0, "daily_milk_litres": 0}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Crop Tasks (Module 2: Crop & Farming Helper)
CREATE TABLE IF NOT EXISTS public.crop_tasks (
    id TEXT PRIMARY KEY,
    farmer_phone TEXT NOT NULL REFERENCES public.farmers(phone) ON DELETE CASCADE,
    crop JSONB NOT NULL,
    title JSONB NOT NULL,
    stage JSONB,
    due_date JSONB,
    priority JSONB,
    status BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_crop_tasks_farmer_phone ON public.crop_tasks(farmer_phone);

-- 3. Livestock Registry & Vaccination History (Module 6)
CREATE TABLE IF NOT EXISTS public.livestock (
    tag_id TEXT PRIMARY KEY,
    farmer_phone TEXT NOT NULL REFERENCES public.farmers(phone) ON DELETE CASCADE,
    name JSONB NOT NULL,
    type JSONB NOT NULL,
    breed JSONB,
    age_years NUMERIC(5, 1),
    daily_milk_yield_litres NUMERIC(6, 2) DEFAULT 0,
    health_status JSONB,
    vaccination_history JSONB DEFAULT '[]'::jsonb,
    production_logs JSONB DEFAULT '[]'::jsonb,
    purchase_date TEXT,
    purchase_price NUMERIC(12, 2),
    pending_completion BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_livestock_farmer_phone ON public.livestock(farmer_phone);

-- 4. Farm Expenses & Income Ledger (Module 7)
CREATE TABLE IF NOT EXISTS public.expenses (
    id TEXT PRIMARY KEY,
    farmer_phone TEXT NOT NULL REFERENCES public.farmers(phone) ON DELETE CASCADE,
    date TEXT NOT NULL,
    month JSONB,
    season JSONB,
    crop JSONB,
    category JSONB NOT NULL,
    description JSONB,
    amount NUMERIC(12, 2) NOT NULL DEFAULT 0,
    payment_mode JSONB,
    entry_type TEXT NOT NULL DEFAULT 'expense' CHECK (entry_type IN ('expense', 'income')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_expenses_farmer_phone ON public.expenses(farmer_phone);
CREATE INDEX IF NOT EXISTS idx_expenses_date ON public.expenses(date DESC);

-- 5. Farmer-to-Buyer Marketplace Listings (Module 5)
CREATE TABLE IF NOT EXISTS public.marketplace_listings (
    id TEXT PRIMARY KEY,
    farmer_phone TEXT REFERENCES public.farmers(phone) ON DELETE SET NULL,
    crop_name JSONB NOT NULL,
    category JSONB,
    variety JSONB,
    quality_grade JSONB,
    quantity_quintals NUMERIC(10, 2) NOT NULL DEFAULT 0,
    expected_price_per_quintal NUMERIC(10, 2) NOT NULL DEFAULT 0,
    seller_name JSONB,
    seller_phone TEXT,
    village JSONB,
    taluka JSONB,
    district JSONB,
    location JSONB,
    harvest_date TEXT,
    status JSONB,
    notes JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_marketplace_farmer_phone ON public.marketplace_listings(farmer_phone);

-- 6. Regional Nearby Agricultural Services (Module 4)
CREATE TABLE IF NOT EXISTS public.nearby_services (
    id TEXT PRIMARY KEY,
    added_by_phone TEXT REFERENCES public.farmers(phone) ON DELETE SET NULL,
    name JSONB NOT NULL,
    category JSONB NOT NULL,
    taluka JSONB,
    district JSONB,
    location JSONB,
    phone TEXT,
    timings JSONB,
    speciality JSONB,
    rating NUMERIC(3, 1) DEFAULT 4.5,
    verified BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- ROW LEVEL SECURITY (RLS) CONFIGURATION
-- ============================================================================
-- Enable RLS on every table so the public Supabase `anon` key cannot read
-- or mutate private farmer records directly from a browser.
-- Trusted server-side Flask backend connects with SUPABASE_SERVICE_ROLE_KEY
-- (which bypasses RLS while enforcing farmer_phone scoping in Python).

ALTER TABLE public.farmers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.crop_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.livestock ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.expenses ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.marketplace_listings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.nearby_services ENABLE ROW LEVEL SECURITY;

-- Public/Anon read-only access ONLY for non-private regional directory & public marketplace
DROP POLICY IF EXISTS "Public can view verified nearby services" ON public.nearby_services;
CREATE POLICY "Public can view verified nearby services"
    ON public.nearby_services FOR SELECT
    TO anon, authenticated
    USING (verified = TRUE);

DROP POLICY IF EXISTS "Public can view marketplace listings" ON public.marketplace_listings;
CREATE POLICY "Public can view marketplace listings"
    ON public.marketplace_listings FOR SELECT
    TO anon, authenticated
    USING (TRUE);

-- Private farmer tables (farmers, crop_tasks, livestock, expenses) have NO public/anon policies,
-- ensuring zero exposure via anon key.

-- ============================================================================
-- TABLE-LEVEL PRIVILEGES (REQUIRED FOR POSTGREST / SUPABASE ROLES)
-- ============================================================================
GRANT USAGE ON SCHEMA public TO service_role, anon, authenticated;

GRANT ALL ON TABLE
    public.farmers,
    public.crop_tasks,
    public.livestock,
    public.expenses,
    public.marketplace_listings,
    public.nearby_services
TO service_role;

GRANT SELECT ON TABLE
    public.marketplace_listings,
    public.nearby_services
TO anon, authenticated;

