from app import create_app
from models import Review

def seed_reviews():
    reviews = [
        {
            "customer_name": "Arif Ahmed",
            "rating": 5,
            "comment": "খুবই ফ্রেশ এবং প্রিমিয়াম কোয়ালিটির হানি নাট। মধুর স্বাদটা একদম ন্যাচারাল।"
        },
        {
            "customer_name": "Sabina Yasmin",
            "rating": 5,
            "comment": "এত ভালো হবে ভাবিনি। বাচ্চার স্বাস্থ্যের জন্য এটা অনেক উপকারী।"
        },
        {
            "customer_name": "Rakibul Islam",
            "rating": 5,
            "comment": "ডেলিভারি অনেক দ্রুত ছিল আর প্যাকিংটাও দারুণ ছিল। রিকমেন্ডেড!"
        },
        {
            "customer_name": "Mehedi Hasan",
            "rating": 5,
            "comment": "অসাধারণ স্বাদ! কাজের ফাঁকে এনার্জি পেতে এটা সেরা।"
        },
        {
            "customer_name": "Farhana Akter",
            "rating": 5,
            "comment": "ড্রাই ফ্রুটসগুলো অনেক ফ্রেশ ছিল। নিউ রয়েল বিডির সার্ভিস সবসময় সেরা।"
        }
    ]

    app = create_app()
    with app.app_context():
        for rev_data in reviews:
            # Check if this review already exists to avoid duplicates
            exists = Review.objects(customer_name=rev_data['customer_name']).first()
            if not exists:
                Review(
                    customer_name=rev_data['customer_name'],
                    rating=rev_data['rating'],
                    comment=rev_data['comment']
                ).save()
                print(f"Added review from {rev_data['customer_name']}")
            else:
                print(f"Skipped existing review from {rev_data['customer_name']}")
        
        print("Successfully seeded reviews for Honey Nut!")

if __name__ == "__main__":
    seed_reviews()