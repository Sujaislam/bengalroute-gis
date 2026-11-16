from django.core.management.base import BaseCommand
from routing.models import Node, Edge

# 32 Major Jelas / Districts across all 8 Divisions of Bangladesh
BANGLADESH_JELA_NODES = [
    # 1. Dhaka Division (ঢাকা বিভাগ)
    {"code": "BD_DHK", "name": "Dhaka",         "bn": "ঢাকা",         "div": "Dhaka",      "lat": 23.8103, "lng": 90.4125, "desc": "National capital and economic heart of Bangladesh"},
    {"code": "BD_GZP", "name": "Gazipur",       "bn": "গাজীপুর",       "div": "Dhaka",      "lat": 24.0023, "lng": 90.4264, "desc": "Industrial hub & northern transport intersection"},
    {"code": "BD_NGJ", "name": "Narayanganj",   "bn": "নারায়ণগঞ্জ",   "div": "Dhaka",      "lat": 23.6238, "lng": 90.5000, "desc": "Historic inland river port & Shitalakshya trade city"},
    {"code": "BD_TNG", "name": "Tangail",       "bn": "টাঙ্গাইল",       "div": "Dhaka",      "lat": 24.2513, "lng": 89.9167, "desc": "Gateway to Jamuna Bridge (Bangabandhu Bridge)"},
    {"code": "BD_FRP", "name": "Faridpur",       "bn": "ফরিদপুর",       "div": "Dhaka",      "lat": 23.6071, "lng": 89.8429, "desc": "Padma Bridge west corridor connecting South Bengal"},
    {"code": "BD_NRD", "name": "Narsingdi",     "bn": "নরসিংদী",     "div": "Dhaka",      "lat": 23.9193, "lng": 90.7176, "desc": "Eastern industrial & textile manufacturing district"},
    {"code": "BD_MNK", "name": "Manikganj",     "bn": "মানিকগঞ্জ",     "div": "Dhaka",      "lat": 23.8617, "lng": 90.0003, "desc": "Aricha ghat approach across the Padma river"},
    {"code": "BD_GPL", "name": "Gopalganj",     "bn": "গোপালগঞ্জ",     "div": "Dhaka",      "lat": 23.0051, "lng": 89.8266, "desc": "South-central district near the Madhumati river"},

    # 2. Chattogram Division (চট্টগ্রাম বিভাগ)
    {"code": "BD_CTG", "name": "Chattogram",    "bn": "চট্টগ্রাম",     "div": "Chattogram", "lat": 22.3569, "lng": 91.7832, "desc": "Principal seaport and commercial capital"},
    {"code": "BD_CXB", "name": "Cox's Bazar",   "bn": "কক্সবাজার",   "div": "Chattogram", "lat": 21.4272, "lng": 92.0058, "desc": "World's longest unbroken natural sandy sea beach"},
    {"code": "BD_COM", "name": "Cumilla",       "bn": "কুমিল্লা",       "div": "Chattogram", "lat": 23.4682, "lng": 91.1788, "desc": "Historic trade center on Dhaka-Chittagong Highway"},
    {"code": "BD_FEN", "name": "Feni",          "bn": "ফেনী",          "div": "Chattogram", "lat": 23.0159, "lng": 91.3976, "desc": "Key transit checkpoint connecting port to capital"},
    {"code": "BD_BRB", "name": "Brahmanbaria",  "bn": "ব্রাহ্মণবাড়িয়া", "div": "Chattogram", "lat": 23.9608, "lng": 91.1115, "desc": "Major natural gas field hub & eastern rail nexus"},
    {"code": "BD_NOA", "name": "Noakhali",      "bn": "নোয়াখালী",      "div": "Chattogram", "lat": 22.8696, "lng": 91.0993, "desc": "Coastal southern district of Chittagong division"},
    {"code": "BD_CHP", "name": "Chandpur",      "bn": "চাঁদপুর",       "div": "Chattogram", "lat": 23.2333, "lng": 90.6667, "desc": "Hilsa fish capital at Padma & Meghna confluence"},

    # 3. Sylhet Division (সিলেট বিভাগ)
    {"code": "BD_SYL", "name": "Sylhet",        "bn": "সিলেট",        "div": "Sylhet",     "lat": 24.8949, "lng": 91.8687, "desc": "Spiritual tea capital & shrine of Hazrat Shah Jalal"},
    {"code": "BD_MLB", "name": "Moulvibazar",   "bn": "মৌলভীবাজার",   "div": "Sylhet",     "lat": 24.4829, "lng": 91.7774, "desc": "Sreemangal tea garden paradise & Lawachara"},
    {"code": "BD_HBJ", "name": "Habiganj",      "bn": "হবিগঞ্জ",      "div": "Sylhet",     "lat": 24.3749, "lng": 91.4155, "desc": "Southwestern tea and natural gas reserve district"},

    # 4. Rajshahi Division (রাজশাহী বিভাগ)
    {"code": "BD_RAJ", "name": "Rajshahi",      "bn": "রাজশাহী",      "div": "Rajshahi",   "lat": 24.3745, "lng": 88.6042, "desc": "Silk City & major education hub on the Padma"},
    {"code": "BD_BOG", "name": "Bogura",        "bn": "বগুড়া",        "div": "Rajshahi",   "lat": 24.8465, "lng": 89.3777, "desc": "Gateway to North Bengal & Mahasthangarh"},
    {"code": "BD_PAB", "name": "Pabna",         "bn": "পাবনা",         "div": "Rajshahi",   "lat": 24.0064, "lng": 89.2372, "desc": "Rooppur Nuclear plant & mental health institute"},
    {"code": "BD_SRJ", "name": "Sirajganj",     "bn": "সিরাজগঞ্জ",     "div": "Rajshahi",   "lat": 24.4534, "lng": 89.7007, "desc": "Western abutment of the Jamuna Bridge"},
    {"code": "BD_NAT", "name": "Natore",        "bn": "নাটোর",        "div": "Rajshahi",   "lat": 24.4206, "lng": 89.0003, "desc": "Historic Uttara Gonobhaban & Kachagolla center"},

    # 5. Rangpur Division (রংপুর বিভাগ)
    {"code": "BD_RNG", "name": "Rangpur",       "bn": "রংপুর",        "div": "Rangpur",    "lat": 25.7439, "lng": 89.2752, "desc": "Divisional headquarters of northern Bangladesh"},
    {"code": "BD_DNJ", "name": "Dinajpur",      "bn": "দিনাজপুর",      "div": "Rangpur",    "lat": 25.6217, "lng": 88.6354, "desc": "Kantajew Temple & agricultural granary"},
    {"code": "BD_GAI", "name": "Gaibandha",     "bn": "গাইবান্ধা",     "div": "Rangpur",    "lat": 25.3288, "lng": 89.5406, "desc": "Brahmaputra river flood-plain district"},

    # 6. Khulna Division (খুলনা বিভাগ)
    {"code": "BD_KLN", "name": "Khulna",        "bn": "খুলনা",        "div": "Khulna",     "lat": 22.8456, "lng": 89.5403, "desc": "Gateway to Sundarbans Mangrove Forest"},
    {"code": "BD_JSH", "name": "Jashore",       "bn": "যশোর",        "div": "Khulna",     "lat": 23.1664, "lng": 89.2081, "desc": "Benapole land port & first liberated district"},
    {"code": "BD_KSH", "name": "Kushtia",       "bn": "কুষ্টিয়া",       "div": "Khulna",     "lat": 23.9013, "lng": 89.1205, "desc": "Lalon Shah sanctuary & Rabindranath Kuthibari"},

    # 7. Barishal Division (বরিশাল বিভাগ)
    {"code": "BD_BAR", "name": "Barishal",      "bn": "বরিশাল",      "div": "Barishal",   "lat": 22.7010, "lng": 90.3535, "desc": "Venice of Bengal with floating guava markets"},
    {"code": "BD_PAT", "name": "Patuakhali",    "bn": "পটুয়াখালী",    "div": "Barishal",   "lat": 22.3596, "lng": 90.3299, "desc": "Gateway to Kuakata Daughter of Sea beach"},

    # 8. Mymensingh Division (ময়মনসিংহ বিভাগ)
    {"code": "BD_MYM", "name": "Mymensingh",    "bn": "ময়মনসিংহ",    "div": "Mymensingh", "lat": 24.7471, "lng": 90.4203, "desc": "Agricultural university & Brahmaputra basin center"},
]

# Highway Connections Between Interconnecting Jelas
BANGLADESH_JELA_EDGES = [
    # Dhaka Hub
    ("BD_DHK", "BD_GZP"),
    ("BD_DHK", "BD_NGJ"),
    ("BD_DHK", "BD_MNK"),
    ("BD_DHK", "BD_FRP"),   # via Padma Bridge corridor
    
    # Dhaka Division Internal
    ("BD_GZP", "BD_TNG"),
    ("BD_GZP", "BD_NRD"),
    ("BD_GZP", "BD_MYM"),
    ("BD_NGJ", "BD_COM"),
    ("BD_NGJ", "BD_CHP"),
    ("BD_NRD", "BD_BRB"),
    ("BD_MNK", "BD_FRP"),
    ("BD_FRP", "BD_GPL"),
    ("BD_FRP", "BD_PAB"),
    ("BD_GPL", "BD_KLN"),
    ("BD_GPL", "BD_BAR"),

    # Tangail & Jamuna Bridge to Rajshahi / North
    ("BD_TNG", "BD_SRJ"),   # Jamuna Bridge
    ("BD_SRJ", "BD_BOG"),
    ("BD_SRJ", "BD_PAB"),
    ("BD_SRJ", "BD_NAT"),

    # Rajshahi Division
    ("BD_BOG", "BD_RNG"),
    ("BD_BOG", "BD_NAT"),
    ("BD_NAT", "BD_RAJ"),
    ("BD_NAT", "BD_PAB"),
    ("BD_RAJ", "BD_KSH"),
    ("BD_PAB", "BD_KSH"),

    # Rangpur Division
    ("BD_RNG", "BD_DNJ"),
    ("BD_RNG", "BD_GAI"),
    ("BD_BOG", "BD_GAI"),

    # Khulna Division
    ("BD_KSH", "BD_JSH"),
    ("BD_JSH", "BD_KLN"),
    
    # Barishal Division
    ("BD_BAR", "BD_PAT"),
    ("BD_BAR", "BD_FRP"),
    ("BD_BAR", "BD_KLN"),

    # Chattogram Division
    ("BD_COM", "BD_FEN"),
    ("BD_COM", "BD_BRB"),
    ("BD_COM", "BD_CHP"),
    ("BD_CHP", "BD_NOA"),
    ("BD_FEN", "BD_NOA"),
    ("BD_FEN", "BD_CTG"),
    ("BD_CTG", "BD_CXB"),

    # Sylhet Division
    ("BD_BRB", "BD_HBJ"),
    ("BD_HBJ", "BD_MLB"),
    ("BD_MLB", "BD_SYL"),
    ("BD_MYM", "BD_SYL"),
]

# Dhaka Metro Micro-Transit Nodes (16 Landmarks)
DHAKA_METRO_NODES = [
    {"code": "DHK_SHB", "name": "Shahbagh",                     "bn": "শাহবাগ",             "div": "Dhaka", "lat": 23.7380, "lng": 90.3957, "desc": "Central cultural hub, BSMMU & National Museum"},
    {"code": "DHK_TSC", "name": "TSC / Dhaka University",       "bn": "টিএসসি / ঢাবি",       "div": "Dhaka", "lat": 23.7324, "lng": 90.3958, "desc": "Dhaka University Campus & Student Center"},
    {"code": "DHK_MTJ", "name": "Motijheel Commercial Area",    "bn": "মতিঝিল",             "div": "Dhaka", "lat": 23.7330, "lng": 90.4172, "desc": "Primary financial district & central bank"},
    {"code": "DHK_FMG", "name": "Farmgate",                     "bn": "ফার্মগেট",           "div": "Dhaka", "lat": 23.7570, "lng": 90.3897, "desc": "Central transit & bus intersection"},
    {"code": "DHK_KRB", "name": "Karwan Bazar",                 "bn": "কারওয়ান বাজার",     "div": "Dhaka", "lat": 23.7516, "lng": 90.3934, "desc": "Major wholesale trade & media complex"},
    {"code": "DHK_D32", "name": "Dhanmondi 32 (Lake)",          "bn": "ধানমন্ডি ৩২",        "div": "Dhaka", "lat": 23.7511, "lng": 90.3776, "desc": "Historic lakeside promenade"},
    {"code": "DHK_D27", "name": "Dhanmondi 27 / Rapa Plaza",    "bn": "ধানমন্ডি ২৭",        "div": "Dhaka", "lat": 23.7538, "lng": 90.3702, "desc": "Mirpur Road shopping concourse"},
    {"code": "DHK_MHK", "name": "Mohakhali Inter-district Hub", "bn": "মহাখালী",            "div": "Dhaka", "lat": 23.7777, "lng": 90.4057, "desc": "Major bus terminal & flyover junction"},
    {"code": "DHK_GL1", "name": "Gulshan-1 Circle",             "bn": "গুলশান ১",           "div": "Dhaka", "lat": 23.7806, "lng": 90.4172, "desc": "Commercial and diplomatic avenue"},
    {"code": "DHK_GL2", "name": "Gulshan-2 Circle",             "bn": "গুলশান ২",           "div": "Dhaka", "lat": 23.7925, "lng": 90.4162, "desc": "Diplomatic enclave center"},
    {"code": "DHK_BAN", "name": "Banani 11",                    "bn": "বনানী",               "div": "Dhaka", "lat": 23.7940, "lng": 90.4043, "desc": "High-end dining and commercial district"},
    {"code": "DHK_M10", "name": "Mirpur-10 Circle",             "bn": "মিরপুর ১০",           "div": "Dhaka", "lat": 23.8070, "lng": 90.3686, "desc": "Key northern transit & Metro Rail interchange"},
    {"code": "DHK_MR1", "name": "Mirpur-1",                     "bn": "মিরপুর ১",            "div": "Dhaka", "lat": 23.7956, "lng": 90.3537, "desc": "Botanical garden & zoo approach"},
    {"code": "DHK_UT3", "name": "Uttara Sector 3 / Airport Rd", "bn": "উত্তরা ৩",           "div": "Dhaka", "lat": 23.8682, "lng": 90.3995, "desc": "Northern residential zone & airport gateway"},
    {"code": "DHK_JFP", "name": "Bashundhara R/A / Jamuna Park","bn": "বসুন্ধরা / যমুনা পার্ক","div": "Dhaka", "lat": 23.8135, "lng": 90.4242, "desc": "Pragati Sarani mega shopping concourse"},
    {"code": "DHK_LAL", "name": "Lalbagh Fort (Old Dhaka)",     "bn": "লালবাগ কেল্লা",       "div": "Dhaka", "lat": 23.7196, "lng": 90.3881, "desc": "Historic 17th-century Mughal fort complex"},
]

DHAKA_METRO_EDGES = [
    ("DHK_SHB", "DHK_TSC"),
    ("DHK_SHB", "DHK_KRB"),
    ("DHK_SHB", "DHK_MTJ"),
    ("DHK_SHB", "DHK_LAL"),
    ("DHK_TSC", "DHK_MTJ"),
    ("DHK_TSC", "DHK_LAL"),
    ("DHK_KRB", "DHK_FMG"),
    ("DHK_KRB", "DHK_D32"),
    ("DHK_FMG", "DHK_D27"),
    ("DHK_FMG", "DHK_MHK"),
    ("DHK_D32", "DHK_D27"),
    ("DHK_D27", "DHK_MR1"),
    ("DHK_MR1", "DHK_M10"),
    ("DHK_MHK", "DHK_GL1"),
    ("DHK_MHK", "DHK_BAN"),
    ("DHK_MHK", "DHK_M10"),
    ("DHK_GL1", "DHK_GL2"),
    ("DHK_GL1", "DHK_JFP"),
    ("DHK_GL2", "DHK_BAN"),
    ("DHK_GL2", "DHK_JFP"),
    ("DHK_BAN", "DHK_UT3"),
    ("DHK_JFP", "DHK_UT3"),
    ("DHK_M10", "DHK_UT3"),
]

class Command(BaseCommand):
    help = "Seeds database with real geographic nodes and navigable edges for Bangladesh Jelas/Districts and Dhaka Metro"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding Bangladesh Jela / District Network into SQLite database..."))

        # 1. Seed Bangladesh Jela / District Network
        self.stdout.write(self.style.NOTICE("\n--- Seeding Bangladesh Jelas / Districts (32 Districts) ---"))
        bd_node_objs = {}
        for item in BANGLADESH_JELA_NODES:
            node, created = Node.objects.update_or_create(
                code=item["code"],
                defaults={
                    "name": item["name"],
                    "bn_name": item["bn"],
                    "division": item["div"],
                    "region": "bangladesh",
                    "latitude": item["lat"],
                    "longitude": item["lng"],
                    "description": item["desc"],
                }
            )
            bd_node_objs[node.code] = node
            action = "Created" if created else "Updated"
            self.stdout.write(f"  [{action}] {node.code}: {node.name} ({node.bn_name}) - {node.division}")

        for src_code, dst_code in BANGLADESH_JELA_EDGES:
            src = bd_node_objs[src_code]
            dst = bd_node_objs[dst_code]
            edge, _ = Edge.objects.get_or_create(
                source=src, destination=dst,
                defaults={"is_bidirectional": True}
            )

        # 2. Seed Dhaka Metropolitan Network
        self.stdout.write(self.style.NOTICE("\n--- Seeding Dhaka Metropolitan Network (16 Hubs) ---"))
        dhk_node_objs = {}
        for item in DHAKA_METRO_NODES:
            node, created = Node.objects.update_or_create(
                code=item["code"],
                defaults={
                    "name": item["name"],
                    "bn_name": item["bn"],
                    "division": item["div"],
                    "region": "dhaka",
                    "latitude": item["lat"],
                    "longitude": item["lng"],
                    "description": item["desc"],
                }
            )
            dhk_node_objs[node.code] = node
            action = "Created" if created else "Updated"
            self.stdout.write(f"  [{action}] {node.code}: {node.name} ({node.bn_name})")

        for src_code, dst_code in DHAKA_METRO_EDGES:
            src = dhk_node_objs[src_code]
            dst = dhk_node_objs[dst_code]
            edge, _ = Edge.objects.get_or_create(
                source=src, destination=dst,
                defaults={"is_bidirectional": True}
            )

        self.stdout.write(self.style.SUCCESS(
            f"\nSeeding complete! Bangladesh Jelas/Districts: {len(bd_node_objs)} districts. Dhaka Metro: {len(dhk_node_objs)} nodes."
        ))
