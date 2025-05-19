print("""
The plan is:

1. For each category, define a set of possible question templates and corresponding answer templates that include boutique-specific details, emojis, and structured information.

2. When generating each FAQ entry, select the category and then choose a question and answer template from that category's pool.

3. Replace placeholders in the templates with the relevant parameters (like size, style, price tier, etc.).

4. Ensure that the answers provide detailed, engaging information that highlights the boutique's strengths, such as craftsmanship, materials, sustainability, and exclusive services.

Additionally, the price tiers in the original code are too low for a boutique. The improved example had higher prices, so adjusting the prices list to something like ["$45-$65", "$85-$120", "$150+"] would be more appropriate.

Also, the current code's parameters (styles, designs) could be expanded. For example, styles could include "casual", "designer", "luxury artisan", etc., and designs could have more boutique-specific terms like "embroidery", "monogramming", "custom collar".

Moreover, the answer should vary more. For example, when the category is "Returns & Exchanges", the answer could mention the 30-day return policy, surprise coupons, etc., similar to the improved example.

In summary, the main steps to improve the code are:

- Restructure the FAQ generation to use category-specific templates for questions and answers.

- Enrich the answer content with boutique-specific details, emojis, and structured info.

- Adjust price tiers and other parameters to reflect a luxury boutique.

- Diversify the questions to cover different aspects beyond just product features.

- Include USP elements like sustainability, custom services, and promotions in answers.

This approach would make each FAQ entry more unique, informative, and aligned with the boutique's brand image.

""")
# This script generates a JSON file containing 100 FAQs for a boutique specializing in cotton shirts.

import json
from datetime import datetime
import random

today = datetime.today().strftime("%Y-%m-%d")

# Enhanced boutique-specific data structures
collections = [
    {
        "name": "🎨 Casual Collection",
        "price_range": "$45-$65",
        "styles": ["linen", "chambray", "oxford"],
        "features": ["relaxed fit", "breathable fabrics", "everyday luxury"]
    },
    {
        "name": "🌟 Premium Designer",
        "price_range": "$85-$120",
        "styles": ["silk-blend", "twill", "jacquard"],
        "features": ["tailored fit", "hand-stitched details", "limited editions"]
    },
    {
        "name": "🎁 Luxury Artisan",
        "price_range": "$150+",
        "styles": ["custom embroidery", "bespoke patterns", "premium cashmere"],
        "features": ["made-to-measure", "consultation included", "heirloom quality"]
    }
]

services = [
    ("VIP Fitting", "🍾 Champagne service with our master tailor", "+$50"),
    ("Eco-Clean", "🌿 Sustainable dry cleaning package", "+$20"),
    ("Monogramming", "✨ Initial embroidery on cuff or collar", "+$35")
]

def generate_boutique_answer(faq_type, collection, style, size):
    """Generate boutique-style answers with rich formatting"""
    base_price = random.choice([45, 85, 150])
    price_range = f"${base_price}-${base_price + random.randint(20, 50)}"
    
    answer_components = {
        "pricing": f"""Our {style} shirts feature:

{collection['name']} ({collection['price_range']})
✨ {random.choice(collection['features'])}
✨ {random.choice(collection['features'])}
✨ Complimentary {random.choice(["wooden hanger", "dust bag", "silk tie clip"])}

Price includes:
✅ Free alterations within 14 days
✅ Sustainable packaging
✅ Style consultation""",

        "care": f"""Maintain your {style} shirt's luxury:

🔹 Professional eco-clean recommended (${random.randint(15, 25)}/service)
🔹 Use our cedar hangers (included)
🔹 Avoid direct sunlight on {random.choice(["embroidery", "delicate fabrics", "metallic details"])}

Book a maintenance session: care@boutique.com""",

        "shipping": f"""✈️ Global shipping options:

Standard (3-5 days): ${random.randint(10, 15)}
Express (2 days): ${random.randint(25, 40)}
Luxury Collection (overnight + gift wrap): ${random.randint(75, 100)}

Orders >$200 get complimentary 📦 premium packaging!"""
    }
    
    return answer_components.get(faq_type, f"Discover boutique excellence in every stitch. Contact us for details.")

# Generate boutique-style FAQs
faq_data = {"faqs": []}

for i in range(1, 501):
    collection = random.choice(collections)
    style = random.choice(collection["styles"])
    size = random.choice(["Slim Fit", "Classic Fit", "Made-to-Measure"])
    faq_type = random.choice(["pricing", "care", "shipping"])
    
    question = random.choice([
        f"How should I care for my {style} {collection['name']} shirt?",
        f"What makes your {collection['name']} collection special?",
        f"Can I get {style} shirts in {size}?",
        f"What's included in the price of {collection['name']} shirts?",
        f"Do you offer international shipping for {style} designs?"
    ])
    
    faq_entry = {
        "id": i,
        "category": collection['name'],
        "tags": [style, size, collection['name'].split()[1]],
        "question": question,
        "answer": generate_boutique_answer(faq_type, collection, style, size),
        "price_range": collection['price_range'],
        "collection": collection['name'],
        "services": random.sample(services, k=2),
        "last_updated": today
    }
    
    faq_data["faqs"].append(faq_entry)

# Save to faqs.json
with open("faqs.json", "w", encoding="utf-8") as f:
    json.dump(faq_data, f, indent=4, ensure_ascii=False)

print(f"{i} Luxury boutique FAQs generated successfully! 🎉")

