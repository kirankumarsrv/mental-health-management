"""Quick script to check created usernames"""
from backend.database import SessionLocal
from backend import models

db = SessionLocal()

print("\n" + "=" * 60)
print("SOLDIER ACCOUNTS (first 10)")
print("=" * 60)

soldiers = db.query(models.User).filter_by(role=models.UserRole.soldier).limit(10).all()
for user in soldiers:
    person = db.query(models.Person).filter_by(id=user.person_id).first()
    print(f"Username: {user.username:25} | Name: {person.name if person else 'N/A'}")

print("\n" + "=" * 60)
print("THERAPIST ACCOUNTS")
print("=" * 60)

therapists = db.query(models.User).filter_by(role=models.UserRole.therapist).all()
for user in therapists:
    therapist = db.query(models.Therapist).filter_by(id=user.therapist_id).first()
    print(f"Username: {user.username:25} | Name: {therapist.name if therapist else 'N/A'}")

print("\n" + "=" * 60)
print(f"Total soldier accounts: {db.query(models.User).filter_by(role=models.UserRole.soldier).count()}")
print("=" * 60)

db.close()
