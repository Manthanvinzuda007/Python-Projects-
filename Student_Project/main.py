# FILE: main.py
from database import Database

def main():
    db = Database() # Database object banavyo

    while True:
        print("\n" + "="*30)
        print("🚀 PROFESSIONAL STUDENT MANAGER")
        print("="*30)
        print("1. Add Student")
        print("2. View All")
        print("3. Delete Student")
        print("4. Exit")
        
        choice = input("👉 Choose Option: ")

        if choice == '1':
            name = input("Enter Name: ").strip()
            course = input("Enter Course: ").strip()
            if name and course:
                student = db.add_student(name, course)
                print(f"✅ Added: {student}")
            else:
                print("❌ Name/Course cannot be empty.")

        elif choice == '2':
            students = db.get_all_students()
            print("\n📋 List of Students:")
            if not students:
                print("   (No data found)")
            for s in students:
                print("   " + str(s))

        elif choice == '3':
            try:
                roll = int(input("Enter Roll No to delete: "))
                if db.delete_student(roll):
                    print(f"✅ Student {roll} deleted successfully.")
                else:
                    print("❌ Student not found.")
            except ValueError:
                print("❌ Please enter valid number.")

        elif choice == '4':
            print("👋 Bye Bye!")
            break
        else:
            print("Invalid Choice.")

if __name__ == "__main__":
    main()