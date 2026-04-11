import os

class Student:
    """Represents a student with marks and grading logic."""
    def __init__(self, roll_no, name, marks):
        self.roll_no = roll_no
        self.name = name
        self.marks = marks  # Dictionary {Subject: Score}

    def average(self):
        """Calculates and returns the average score across all subjects."""
        if not self.marks:
            return 0.0
        return sum(self.marks.values()) / len(self.marks)

    def grade(self):
        """Returns a letter grade based on the average score."""
        avg = self.average()
        if avg >= 80: return 'A'
        if avg >= 70: return 'B'
        if avg >= 60: return 'C'
        if avg >= 50: return 'D'
        return 'F'

    def __str__(self):
        """Returns a neat single-line summary of the student."""
        return f"Roll: {self.roll_no} | Name: {self.name:<15} | Avg: {self.average():.2f} | Grade: {self.grade()}"

# --- Feature 2: Data Storage & File Persistence ---

def save_all(students, filename="records.txt"):
    """Writes all student records to the file in CSV-style format."""
    try:
        with open(filename, "w") as f:
            for s in students:
                # Join marks into Subject:Score format
                marks_str = ",".join([f"{sub}:{score}" for sub, score in s.marks.items()])
                f.write(f"{s.roll_no},{s.name},{marks_str}\n")
    except IOError as e:
        print(f"Error saving to file: {e}")

def load_all(filename="records.txt"):
    """Reads the file and returns a list of Student objects."""
    students = []
    if not os.path.exists(filename):
        return students
    try:
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) < 3: continue
                roll, name = parts[0], parts[1]
                marks = {}
                for m in parts[2:]:
                    sub, score = m.split(':')
                    marks[sub] = float(score)
                students.append(Student(roll, name, marks))
    except Exception as e:
        print(f"Error loading data: {e}")
    return students

# --- Feature 4: Analytics ---

def show_statistics(students):
    """Displays comprehensive class-wide analytics."""
    if not students:
        print("\n[!] No data available to show statistics.")
        return

    total = len(students)
    averages = [s.average() for s in students]
    class_avg = sum(averages) / total
    
    # Grade distribution logic
    grades = [s.grade() for s in students]
    dist = {g: grades.count(g) for g in ['A', 'B', 'C', 'D', 'F']}
    
    top_s = max(students, key=lambda s: s.average())
    low_s = min(students, key=lambda s: s.average())

    # Subject performance logic
    sub_totals = {}
    sub_counts = {}
    for s in students:
        for sub, score in s.marks.items():
            sub_totals[sub] = sub_totals.get(sub, 0) + score
            sub_counts[sub] = sub_counts.get(sub, 0) + 1
    
    best_sub = max(sub_totals, key=lambda k: sub_totals[k]/sub_counts[k])

    print("\n--- Class Statistics ---")
    print(f"Total Students:    {total}")
    print(f"Class Average:     {class_avg:.2f}")
    print(f"Top Performer:     {top_s.name} ({top_s.average():.2f})")
    print(f"Lowest Scorer:     {low_s.name} ({low_s.average():.2f})")
    print(f"Grade Distribution: {dist}")
    print(f"Best Subject:      {best_sub}")

# --- Feature 3: Menu System & Input Validation ---

def get_valid_marks():
    """Prompts for marks and validates they are numeric and 0-100."""
    marks = {}
    while True:
        sub = input("Enter subject (or 'done'): ").strip()
        if sub.lower() == 'done': break
        if not sub: continue
        try:
            val = float(input(f"Enter marks for {sub}: "))
            if 0 <= val <= 100:
                marks[sub] = val
            else:
                print("Marks must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Enter a numeric value.")
    return marks

def main():
    """Main program loop and menu interface."""
    students = load_all()
    
    while True:
        print("\n=== Student Management System ===")
        print("1. Add new student\n2. View all students\n3. Search by roll number")
        print("4. Delete a student\n5. Show top performer\n6. Show class statistics\n0. Exit")
        
        choice = input("\nSelect an option: ")

        if choice == '1':
            roll = input("Enter Roll Number: ").strip()
            if any(s.roll_no == roll for s in students) or not roll:
                print("Error: Roll number must be unique and non-empty.")
                continue
            name = input("Enter Name: ").strip()
            if not name:
                print("Error: Name cannot be empty.")
                continue
            marks = get_valid_marks()
            if marks:
                students.append(Student(roll, name, marks))
                save_all(students)
                print("Student added successfully!")

        elif choice == '2':
            print("\n--- Student Records ---")
            for s in students: print(s)

        elif choice == '3':
            roll = input("Enter Roll No to search: ")
            found = next((s for s in students if s.roll_no == roll), None)
            print(f"\nResult: {found}" if found else "\n[!] Student not found.")

        elif choice == '4':
            roll = input("Enter Roll No to delete: ")
            before = len(students)
            students = [s for s in students if s.roll_no != roll]
            if len(students) < before:
                save_all(students)
                print("Record deleted.")
            else:
                print("[!] Roll number not found.")

        elif choice == '5':
            if students:
                top = max(students, key=lambda s: s.average())
                print(f"\nTop Performer: {top}")
            else:
                print("\n[!] No records found.")

        elif choice == '6':
            show_statistics(students)

        elif choice == '0':
            print("Exiting System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()