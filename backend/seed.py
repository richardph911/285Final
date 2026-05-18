import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'votes.db')

conn = sqlite3.connect(DB_PATH)
conn.executescript('''
    CREATE TABLE IF NOT EXISTS items (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        cuisine TEXT,
        image_url TEXT,
        emoji TEXT
    );
    CREATE TABLE IF NOT EXISTS votes (
        id TEXT PRIMARY KEY,
        item_id TEXT NOT NULL,
        session_id TEXT NOT NULL,
        choice TEXT NOT NULL CHECK(choice IN ('yes', 'no')),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(item_id, session_id),
        FOREIGN KEY(item_id) REFERENCES items(id)
    );
''')

foods = [
    # Italian
    ('f001','Margherita Pizza','Classic tomato, mozzarella, fresh basil on thin crust','Italian','🍕'),
    ('f002','Spaghetti Carbonara','Creamy egg sauce with pancetta and pecorino romano','Italian','🍝'),
    ('f003','Tiramisu','Espresso-soaked ladyfingers with mascarpone cream','Italian','🍰'),
    ('f004','Lasagna','Layered pasta with rich meat sauce and béchamel','Italian','🫕'),
    ('f005','Risotto ai Funghi','Creamy Arborio rice with wild mushrooms and parmesan','Italian','🍚'),
    ('f006','Focaccia','Pillowy olive oil flatbread with rosemary and sea salt','Italian','🫓'),
    ('f007','Arancini','Crispy fried rice balls stuffed with ragù and cheese','Italian','🧆'),
    ('f008','Caprese Salad','Fresh tomato, burrata, basil and aged balsamic','Italian','🥗'),
    # Japanese
    ('f009','Tonkotsu Ramen','Rich pork bone broth with chashu, egg and nori','Japanese','🍜'),
    ('f010','Sushi Omakase',"Chef's selection of premium nigiri and sashimi",'Japanese','🍣'),
    ('f011','Takoyaki','Octopus balls with bonito flakes and okonomiyaki sauce','Japanese','🐙'),
    ('f012','Katsu Curry','Crispy breaded pork cutlet over Japanese curry rice','Japanese','🍛'),
    ('f013','Gyoza','Pan-fried dumplings with ginger pork filling','Japanese','🥟'),
    ('f014','Matcha Ice Cream','Ceremonial grade matcha soft serve','Japanese','🍦'),
    ('f015','Yakitori','Charcoal-grilled chicken skewers with tare sauce','Japanese','🍢'),
    ('f016','Okonomiyaki','Savory pancake with cabbage, seafood and Japanese mayo','Japanese','🥞'),
    # Mexican
    ('f017','Tacos al Pastor','Spit-roasted pork with pineapple on corn tortillas','Mexican','🌮'),
    ('f018','Guacamole','Chunky avocado with lime, cilantro and jalapeño','Mexican','🥑'),
    ('f019','Chilaquiles','Crispy tortilla chips in salsa verde with crema','Mexican','🫔'),
    ('f020','Elote','Grilled corn slathered with cotija, chili and lime','Mexican','🌽'),
    ('f021','Mole Negro','Complex dark sauce with 30+ ingredients over chicken','Mexican','🍗'),
    ('f022','Churros','Fried dough sticks with cinnamon sugar and chocolate dip','Mexican','🍩'),
    ('f023','Pozole Rojo','Hearty hominy soup with pork and dried chili broth','Mexican','🍲'),
    ('f024','Tamales','Masa dough with filling steamed in corn husks','Mexican','🫔'),
    # Indian
    ('f025','Butter Chicken','Tender chicken in velvety tomato-cream sauce','Indian','🍛'),
    ('f026','Biryani','Fragrant basmati rice layered with spiced meat','Indian','🍚'),
    ('f027','Samosa','Crispy pastry filled with spiced potato and peas','Indian','🥟'),
    ('f028','Dosa','Fermented rice crepe with coconut chutney and sambar','Indian','🫓'),
    ('f029','Pani Puri','Hollow crispy shells filled with tangy tamarind water','Indian','🫧'),
    ('f030','Naan','Tandoor-baked flatbread with garlic and butter','Indian','🫓'),
    ('f031','Palak Paneer','Fresh cheese cubes in creamy spiced spinach sauce','Indian','🥬'),
    ('f032','Gulab Jamun','Soft milk dumplings soaked in rose-cardamom syrup','Indian','🍮'),
    # Chinese
    ('f033','Peking Duck','Lacquered roasted duck with pancakes and hoisin','Chinese','🦆'),
    ('f034','Dim Sum Basket','Assorted steamed dumplings and bao from the cart','Chinese','🥟'),
    ('f035','Mapo Tofu','Silken tofu in fiery Sichuan peppercorn sauce','Chinese','🌶️'),
    ('f036','Kung Pao Chicken','Wok-tossed chicken with peanuts and dried chili','Chinese','🥜'),
    ('f037','Soup Dumplings','Xiao long bao bursting with pork and rich broth','Chinese','🥟'),
    ('f038','Dan Dan Noodles','Spicy sesame noodles with minced pork and scallions','Chinese','🍜'),
    ('f039','Char Siu Pork','Cantonese BBQ pork with sweet caramelized crust','Chinese','🍖'),
    ('f040','Egg Tart','Buttery pastry shell with silky egg custard filling','Chinese','🥧'),
    # American
    ('f041','Smash Burger','Double smashed patty with American cheese and special sauce','American','🍔'),
    ('f042','BBQ Brisket','14-hour smoked Texas-style brisket with bark crust','American','🥩'),
    ('f043','Lobster Roll','Maine lobster with mayo on a buttered split-top bun','American','🦞'),
    ('f044','Nashville Hot Chicken','Cayenne-drenched fried chicken on white bread and pickles','American','🍗'),
    ('f045','New York Cheesecake','Dense creamy cheesecake on graham cracker crust','American','🍰'),
    ('f046','Clam Chowder','Creamy New England chowder in a sourdough bread bowl','American','🍲'),
    ('f047','Mac and Cheese','Baked elbow pasta in four-cheese béchamel with breadcrumbs','American','🧀'),
    ('f048','Pancake Stack','Fluffy buttermilk pancakes with maple syrup and butter','American','🥞'),
    # Thai
    ('f049','Pad Thai','Wok-fried rice noodles with shrimp, peanuts and tamarind','Thai','🍜'),
    ('f050','Green Curry','Aromatic coconut milk curry with Thai basil and eggplant','Thai','🍛'),
    ('f051','Som Tum','Shredded green papaya salad with fish sauce and chili','Thai','🥗'),
    ('f052','Mango Sticky Rice','Sweet coconut sticky rice with fresh ripe mango','Thai','🥭'),
    ('f053','Tom Yum Soup','Hot and sour lemongrass broth with shrimp and mushrooms','Thai','🍲'),
    ('f054','Massaman Curry','Rich curry with potatoes, peanuts and warming spices','Thai','🥜'),
    ('f055','Thai Iced Tea','Strong black tea with sweetened condensed milk over ice','Thai','🧋'),
    ('f056','Larb','Minced meat salad with toasted rice, herbs and lime','Thai','🥗'),
    # French
    ('f057','Croissant','Buttery laminated pastry with shatteringly crisp layers','French','🥐'),
    ('f058','French Onion Soup','Caramelized onion broth with gruyère crouton','French','🧅'),
    ('f059','Crème Brûlée','Silky vanilla custard with crackling caramelized sugar','French','🍮'),
    ('f060','Beef Bourguignon','Slow-braised beef in red wine with pearl onions','French','🥩'),
    ('f061','Ratatouille','Provençal vegetable stew with tomato and herbes de Provence','French','🍆'),
    ('f062','Macaron','Delicate almond meringue sandwich cookies in pastel colors','French','🫧'),
    ('f063','Steak Frites','Entrecôte with crispy double-fried frites and béarnaise','French','🥩'),
    ('f064','Soufflé au Chocolat','Cloud-light molten chocolate soufflé fresh from the oven','French','🍫'),
    # Korean
    ('f065','Korean BBQ','Tableside grilled marinated short ribs with banchan','Korean','🥩'),
    ('f066','Bibimbap','Stone pot rice with vegetables, egg and gochujang','Korean','🍲'),
    ('f067','Korean Fried Chicken','Double-fried chicken glazed with sticky sweet-spicy sauce','Korean','🍗'),
    ('f068','Tteokbokki','Chewy rice cakes in fiery gochujang sauce with fish cake','Korean','🌶️'),
    ('f069','Kimchi Jjigae','Deeply funky fermented kimchi stew with pork and tofu','Korean','🥘'),
    ('f070','Japchae','Silky glass noodles stir-fried with vegetables and sesame','Korean','🍜'),
    ('f071','Bingsu','Shaved milk ice with red bean, mochi and condensed milk','Korean','🧊'),
    ('f072','Sundubu Jjigae','Silken tofu soup with seafood in spicy broth','Korean','🍲'),
    # Middle Eastern
    ('f073','Shawarma','Slow-roasted spiced lamb in flatbread with garlic sauce','Middle Eastern','🌯'),
    ('f074','Hummus','Smooth chickpea dip with olive oil and smoked paprika','Middle Eastern','🫘'),
    ('f075','Falafel','Crispy fried chickpea balls with tahini and pickled turnip','Middle Eastern','🧆'),
    ('f076','Baklava','Honey-soaked phyllo layers with pistachios and rose water','Middle Eastern','🍯'),
    ('f077','Mansaf','Jordanian lamb in fermented yogurt sauce over fragrant rice','Middle Eastern','🍚'),
    ('f078','Knafeh','Crispy shredded wheat with stretchy white cheese and syrup','Middle Eastern','🧀'),
    # Spanish
    ('f079','Paella Valenciana','Saffron rice with rabbit, chicken and green beans','Spanish','🥘'),
    ('f080','Patatas Bravas','Crispy potato cubes with smoky brava sauce and aioli','Spanish','🥔'),
    ('f081','Jamón Ibérico','Hand-carved acorn-fed Iberian ham with pan con tomate','Spanish','🥩'),
    ('f082','Gazpacho','Chilled raw tomato soup with cucumber and sherry vinegar','Spanish','🍅'),
    ('f083','Pintxos','Basque-style bar snacks on crusty bread with toothpicks','Spanish','🍢'),
    # Vietnamese
    ('f084','Pho Bo','Slow-cooked beef bone broth with rice noodles and herbs','Vietnamese','🍜'),
    ('f085','Bánh Mì','Baguette with pâté, pickled daikon, jalapeño and cilantro','Vietnamese','🥖'),
    ('f086','Bún Bò Huế','Spicy lemongrass beef noodle soup with thick round noodles','Vietnamese','🍲'),
    ('f087','Gỏi Cuốn','Fresh rice paper rolls with shrimp, herb and peanut sauce','Vietnamese','🌯'),
    ('f088','Cà Phê Trứng','Hanoi egg coffee with whipped egg yolk and condensed milk','Vietnamese','☕'),
    # Greek
    ('f089','Moussaka','Baked eggplant and spiced lamb with béchamel crust','Greek','🫕'),
    ('f090','Spanakopita','Flaky phyllo pie with spinach and feta cheese','Greek','🥧'),
    ('f091','Souvlaki','Grilled pork skewers with pita, tzatziki and tomato','Greek','🍢'),
    ('f092','Greek Salad','Chunky tomato, cucumber, kalamata olives and block feta','Greek','🥗'),
    # Ethiopian
    ('f093','Injera & Wats','Sourdough flatbread with spiced lentil and meat stews','Ethiopian','🫓'),
    ('f094','Kitfo','Ethiopian spiced minced raw beef with mitmita butter','Ethiopian','🥩'),
    # Peruvian
    ('f095','Ceviche',"Tiger's milk-cured fish with aji amarillo and sweet potato",'Peruvian','🐟'),
    ('f096','Lomo Saltado','Stir-fried beef with tomato, onion and French fries','Peruvian','🥩'),
    # Misc
    ('f097','Chocolate Lava Cake','Warm dark chocolate cake with molten center and vanilla ice cream','Dessert','🍫'),
    ('f098','Truffle Fries','Crispy shoestring fries tossed in truffle oil and parmesan','Sides','🍟'),
    ('f099','Wagyu Beef Sushi','A5 Wagyu beef nigiri barely kissed by the flame','Japanese','🍣'),
    ('f100','Açaí Bowl','Frozen açaí purée topped with granola, banana and honey','Brazilian','🫐'),
]

for (fid, name, desc, cuisine, emoji) in foods:
    image_url = f"https://source.unsplash.com/400x500/?food,{name.split()[0].lower()}"
    conn.execute(
        'INSERT OR IGNORE INTO items (id, name, description, cuisine, image_url, emoji) VALUES (?,?,?,?,?,?)',
        (fid, name, desc, cuisine, image_url, emoji)
    )

conn.commit()
conn.close()
print(f"✅ Seeded {len(foods)} food items")
