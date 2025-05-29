from models import PRODUCT, PRODUCT_PLASTIC_REQUIREMENTS,PRODUCT_REQUIREMENTS, DB

def create_product(google, microsoft):
    
    blue_pen = PRODUCT(
        customer_id = google.id,

        company_product_name = "sophesticated instrument of blue writing",
        local_product_name = "blue pen"
    )
    green_pen = PRODUCT(
        customer_id = google.id,

        company_product_name = "sophesticated instrument of green writing",
        local_product_name = "green pen"
    )
    metallic_mouse = PRODUCT(
        customer_id = google.id,

        company_product_name = "wakakawa",
        local_product_name = "wak"
    )
    plastic_mouse = PRODUCT(
        customer_id = microsoft.id,

        company_product_name = "plastic_mouse model fmewiojq398f",
        local_product_name = "mouse"
    )
    assembly_mouse = PRODUCT(
        customer_id = microsoft.id,

        company_product_name = "assembly_mouse model fmewiojq398f",
        local_product_name = "assembly mouse"
    )
    DB.session.add_all([blue_pen, green_pen,metallic_mouse,plastic_mouse,assembly_mouse])
    DB.session.commit()