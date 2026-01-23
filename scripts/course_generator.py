"""
Interactive Course Generator
============================
Generates complete interactive courses from topic input.

Usage:
    python course_generator.py --topic "Primavera P6" --level "advanced" --duration "full"
    python course_generator.py --interactive
"""

import os
import json
import argparse
from datetime import datetime
from typing import List, Dict

# ============================================================
# CONFIGURATION
# ============================================================

OUTPUT_BASE = r"d:\my-dev-knowledge-base\courses"
TEMPLATE_DIR = r"d:\my-dev-knowledge-base\templates\course-template"

# ============================================================
# COURSE STRUCTURE GENERATOR
# ============================================================

class CourseGenerator:
    """Generate interactive courses from topic."""
    
    def __init__(self, topic: str, level: str = "intermediate", 
                 duration: str = "full", output_format: str = "both"):
        self.topic = topic
        self.level = level.lower()
        self.duration = duration.lower()
        self.output_format = output_format.lower()
        self.course_id = self._generate_id()
        self.output_dir = os.path.join(OUTPUT_BASE, self.course_id)
        
    def _generate_id(self) -> str:
        """Generate course folder name."""
        clean = self.topic.lower()
        for char in ['&', ',', '.', ':', ';', '/', '\\', ' ']:
            clean = clean.replace(char, '-')
        while '--' in clean:
            clean = clean.replace('--', '-')
        return clean[:50]
    
    def generate_outline(self) -> Dict:
        """Generate course structure based on duration."""
        
        # Duration presets
        presets = {
            "micro": {"modules": 2, "lessons_per_module": 2, "quiz_questions": 5},
            "short": {"modules": 4, "lessons_per_module": 3, "quiz_questions": 8},
            "full": {"modules": 6, "lessons_per_module": 4, "quiz_questions": 10}
        }
        
        config = presets.get(self.duration, presets["full"])
        
        outline = {
            "title": f"{self.topic} Course",
            "id": self.course_id,
            "level": self.level,
            "duration": self.duration,
            "created": datetime.now().isoformat(),
            "learning_outcomes": self._generate_outcomes(),
            "modules": []
        }
        
        # Generate modules
        module_topics = self._generate_module_topics(config["modules"])
        
        for i, module_topic in enumerate(module_topics, 1):
            module = {
                "id": f"module-{i:02d}",
                "title": module_topic,
                "lessons": [],
                "quiz": {"questions": []},
                "practical": {}
            }
            
            # Generate lessons
            lesson_topics = self._generate_lesson_topics(module_topic, config["lessons_per_module"])
            for j, lesson_topic in enumerate(lesson_topics, 1):
                module["lessons"].append({
                    "id": f"lesson-{i:02d}-{j:02d}",
                    "title": lesson_topic,
                    "content": self._generate_lesson_placeholder(lesson_topic)
                })
            
            # Generate quiz questions
            module["quiz"]["questions"] = self._generate_quiz_questions(
                module_topic, config["quiz_questions"]
            )
            
            # Generate practical
            module["practical"] = self._generate_practical(module_topic, i)
            
            outline["modules"].append(module)
        
        # Add assessments
        outline["assessments"] = {
            "pre_assessment": self._generate_assessment("pre"),
            "final_assessment": self._generate_assessment("final")
        }
        
        return outline
    
    def _generate_outcomes(self) -> List[str]:
        """Generate learning outcomes using Bloom's verbs."""
        blooms_verbs = {
            "beginner": ["identify", "describe", "explain", "recognize"],
            "intermediate": ["apply", "demonstrate", "implement", "analyze"],
            "advanced": ["evaluate", "design", "optimize", "integrate"]
        }
        
        verbs = blooms_verbs.get(self.level, blooms_verbs["intermediate"])
        
        return [
            f"{verbs[0].capitalize()} core concepts of {self.topic}",
            f"{verbs[1].capitalize()} key techniques and methodologies",
            f"{verbs[2].capitalize()} practical applications in real scenarios",
            f"{verbs[3].capitalize()} best practices and advanced features"
        ]
    
    def _generate_module_topics(self, count: int) -> List[str]:
        """Generate module topics based on course topic."""
        # Generic module structure
        base_modules = [
            f"Introduction to {self.topic}",
            f"Core Concepts and Fundamentals",
            f"Practical Application",
            f"Advanced Techniques",
            f"Best Practices",
            f"Real-World Projects",
            f"Assessment and Certification"
        ]
        return base_modules[:count]
    
    def _generate_lesson_topics(self, module: str, count: int) -> List[str]:
        """Generate lesson topics for a module."""
        return [f"{module} - Part {i}" for i in range(1, count + 1)]
    
    def _generate_lesson_placeholder(self, topic: str) -> str:
        """Generate lesson content placeholder."""
        return f"""
## {topic}

### Overview
[Content about {topic}]

### Key Concepts
1. [Concept 1]
2. [Concept 2]
3. [Concept 3]

### Examples
[Practical examples demonstrating the concepts]

### Summary
- Key takeaway 1
- Key takeaway 2
"""
    
    def _generate_quiz_questions(self, topic: str, count: int) -> List[Dict]:
        """Generate quiz questions."""
        questions = []
        for i in range(1, count + 1):
            questions.append({
                "id": f"q{i}",
                "type": "multiple-choice",
                "question": f"Question {i} about {topic}?",
                "options": [
                    f"Option A - correct answer",
                    f"Option B - incorrect",
                    f"Option C - incorrect",
                    f"Option D - incorrect"
                ],
                "correct": 0,
                "explanation": f"Explanation for question {i}..."
            })
        return questions
    
    def _generate_practical(self, topic: str, module_num: int) -> Dict:
        """Generate practical exercise."""
        return {
            "title": f"Practical Exercise {module_num}: {topic}",
            "objective": f"Apply {topic} concepts in a hands-on scenario",
            "scenario": f"You are working on a project that requires {topic}...",
            "tasks": [
                {"task": "Task 1: Setup environment", "steps": []},
                {"task": "Task 2: Implement solution", "steps": []},
                {"task": "Task 3: Verify results", "steps": []}
            ],
            "time_limit": "30 minutes",
            "deliverables": ["Completed exercise file", "Screenshot of results"]
        }
    
    def _generate_assessment(self, assessment_type: str) -> Dict:
        """Generate pre or final assessment."""
        if assessment_type == "pre":
            return {
                "title": "Pre-Course Assessment",
                "description": "Test your current knowledge",
                "time_limit": "15 minutes",
                "questions": 10,
                "passing_score": "N/A"
            }
        else:
            return {
                "title": "Final Assessment",
                "description": "Demonstrate your mastery",
                "time_limit": "60 minutes", 
                "questions": 30,
                "passing_score": "80%"
            }
    
    # ============================================================
    # OUTPUT GENERATORS
    # ============================================================
    
    def create_folder_structure(self):
        """Create course folder structure."""
        folders = [
            self.output_dir,
            os.path.join(self.output_dir, "modules"),
            os.path.join(self.output_dir, "quizzes"),
            os.path.join(self.output_dir, "practicals"),
            os.path.join(self.output_dir, "assessments"),
            os.path.join(self.output_dir, "assets", "images"),
            os.path.join(self.output_dir, "assets", "css"),
            os.path.join(self.output_dir, "assets", "js"),
        ]
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
        print(f"✓ Created folder structure: {self.output_dir}")
    
    def generate_markdown(self, outline: Dict):
        """Generate Markdown course files."""
        
        # README.md - Course overview
        readme = f"""# {outline['title']}

**Level**: {outline['level'].title()}
**Duration**: {outline['duration'].title()}
**Created**: {outline['created'][:10]}

---

## Learning Outcomes

By completing this course, you will be able to:

"""
        for i, outcome in enumerate(outline['learning_outcomes'], 1):
            readme += f"{i}. {outcome}\n"
        
        readme += "\n---\n\n## Course Content\n\n"
        
        for module in outline['modules']:
            readme += f"### {module['title']}\n\n"
            for lesson in module['lessons']:
                readme += f"- [{lesson['title']}](modules/{module['id']}/{lesson['id']}.md)\n"
            readme += f"- [Quiz](quizzes/{module['id']}-quiz.md)\n"
            readme += f"- [Practical](practicals/{module['id']}-practical.md)\n\n"
        
        readme += """---

## Assessments

- [Pre-Assessment](assessments/pre-assessment.md)
- [Final Assessment](assessments/final-assessment.md)

---

**Good luck with your learning!** 🎓
"""
        
        with open(os.path.join(self.output_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme)
        
        # Generate module files
        for module in outline['modules']:
            module_dir = os.path.join(self.output_dir, "modules", module['id'])
            os.makedirs(module_dir, exist_ok=True)
            
            for lesson in module['lessons']:
                lesson_content = f"# {lesson['title']}\n\n{lesson['content']}"
                with open(os.path.join(module_dir, f"{lesson['id']}.md"), "w", encoding="utf-8") as f:
                    f.write(lesson_content)
        
            # Generate quiz
            quiz_content = f"# Quiz: {module['title']}\n\n"
            for q in module['quiz']['questions']:
                quiz_content += f"### {q['question']}\n\n"
                for i, opt in enumerate(q['options']):
                    marker = "[x]" if i == q['correct'] else "[ ]"
                    quiz_content += f"- {marker} {chr(65+i)}) {opt}\n"
                quiz_content += f"\n> **Explanation**: {q['explanation']}\n\n---\n\n"
            
            with open(os.path.join(self.output_dir, "quizzes", f"{module['id']}-quiz.md"), "w", encoding="utf-8") as f:
                f.write(quiz_content)
            
            # Generate practical
            prac = module['practical']
            prac_content = f"""# {prac['title']}

## Objective
{prac['objective']}

## Scenario
{prac['scenario']}

## Tasks

"""
            for task in prac['tasks']:
                prac_content += f"### {task['task']}\n\n"
            
            prac_content += f"""
## Time Limit
{prac['time_limit']}

## Deliverables
"""
            for d in prac['deliverables']:
                prac_content += f"- {d}\n"
            
            with open(os.path.join(self.output_dir, "practicals", f"{module['id']}-practical.md"), "w", encoding="utf-8") as f:
                f.write(prac_content)
        
        print(f"✓ Generated Markdown files")
    
    def generate_html(self, outline: Dict):
        """Generate HTML interactive course."""
        
        # index.html
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{outline['title']}</title>
    <link rel="stylesheet" href="assets/css/course.css">
</head>
<body>
    <header>
        <h1>{outline['title']}</h1>
        <p class="meta">Level: {outline['level'].title()} | Duration: {outline['duration'].title()}</p>
    </header>
    
    <nav id="course-nav">
        <h2>Course Content</h2>
        <ul>
"""
        for module in outline['modules']:
            html += f'            <li><a href="modules/{module["id"]}.html">{module["title"]}</a></li>\n'
        
        html += """        </ul>
    </nav>
    
    <main>
        <section id="outcomes">
            <h2>Learning Outcomes</h2>
            <ul>
"""
        for outcome in outline['learning_outcomes']:
            html += f"                <li>{outcome}</li>\n"
        
        html += """            </ul>
        </section>
        
        <section id="start">
            <a href="assessments/pre-assessment.html" class="btn">Start Pre-Assessment</a>
        </section>
    </main>
    
    <script src="assets/js/course.js"></script>
</body>
</html>
"""
        with open(os.path.join(self.output_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        
        # CSS
        css = """
:root {
    --primary: #4a90d9;
    --secondary: #2c3e50;
    --accent: #27ae60;
    --bg: #f8f9fa;
    --text: #333;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: 'Segoe UI', Tahoma, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
}

header {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: white;
    padding: 2rem;
    text-align: center;
}

nav {
    background: white;
    padding: 1rem 2rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

nav ul { list-style: none; }
nav li { margin: 0.5rem 0; }
nav a { color: var(--primary); text-decoration: none; }
nav a:hover { text-decoration: underline; }

main { max-width: 900px; margin: 2rem auto; padding: 0 1rem; }

section { background: white; padding: 2rem; margin: 1rem 0; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }

.btn {
    display: inline-block;
    background: var(--accent);
    color: white;
    padding: 1rem 2rem;
    border-radius: 4px;
    text-decoration: none;
    font-weight: bold;
}

.btn:hover { opacity: 0.9; }

.quiz-container { margin: 1rem 0; }
.question { background: #f0f0f0; padding: 1rem; margin: 1rem 0; border-radius: 4px; }
.options label { display: block; margin: 0.5rem 0; cursor: pointer; }
.feedback { padding: 1rem; margin-top: 1rem; border-radius: 4px; }
.correct { background: #d4edda; color: #155724; }
.incorrect { background: #f8d7da; color: #721c24; }
"""
        os.makedirs(os.path.join(self.output_dir, "assets", "css"), exist_ok=True)
        with open(os.path.join(self.output_dir, "assets", "css", "course.css"), "w", encoding="utf-8") as f:
            f.write(css)
        
        # JavaScript quiz engine
        js = """
// Quiz Engine
class QuizEngine {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.score = 0;
        this.total = 0;
    }
    
    checkAnswer(questionId, selected, correct) {
        this.total++;
        const feedback = document.querySelector(`#${questionId} .feedback`);
        
        if (selected === correct) {
            this.score++;
            feedback.className = 'feedback correct';
            feedback.textContent = '✓ Correct!';
        } else {
            feedback.className = 'feedback incorrect';
            feedback.textContent = '✗ Incorrect. Try again!';
        }
        feedback.style.display = 'block';
    }
    
    showResults() {
        const percent = Math.round((this.score / this.total) * 100);
        alert(`Your score: ${this.score}/${this.total} (${percent}%)`);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    window.quiz = new QuizEngine('quiz-container');
    
    // Add click handlers to all options
    document.querySelectorAll('.options input').forEach(input => {
        input.addEventListener('change', (e) => {
            const question = e.target.closest('.question');
            const correct = parseInt(question.dataset.correct);
            const selected = parseInt(e.target.value);
            window.quiz.checkAnswer(question.id, selected, correct);
        });
    });
});
"""
        os.makedirs(os.path.join(self.output_dir, "assets", "js"), exist_ok=True)
        with open(os.path.join(self.output_dir, "assets", "js", "course.js"), "w", encoding="utf-8") as f:
            f.write(js)
        
        print(f"✓ Generated HTML files")
    
    def save_outline(self, outline: Dict):
        """Save course outline as JSON."""
        with open(os.path.join(self.output_dir, "course-outline.json"), "w", encoding="utf-8") as f:
            json.dump(outline, f, indent=2)
        print(f"✓ Saved course outline JSON")
    
    def generate(self):
        """Main generation method."""
        print(f"\n{'='*60}")
        print(f"GENERATING COURSE: {self.topic}")
        print(f"{'='*60}")
        print(f"Level: {self.level}")
        print(f"Duration: {self.duration}")
        print(f"Format: {self.output_format}")
        print(f"Output: {self.output_dir}")
        print(f"{'='*60}\n")
        
        # Create structure
        self.create_folder_structure()
        
        # Generate outline
        outline = self.generate_outline()
        self.save_outline(outline)
        
        # Generate outputs
        if self.output_format in ["markdown", "both"]:
            self.generate_markdown(outline)
        
        if self.output_format in ["html", "both"]:
            self.generate_html(outline)
        
        print(f"\n{'='*60}")
        print("COURSE GENERATED SUCCESSFULLY!")
        print(f"{'='*60}")
        print(f"\nOutput folder: {self.output_dir}")
        print(f"\nTo view HTML course: Open {os.path.join(self.output_dir, 'index.html')}")
        print(f"To view Markdown: Open {os.path.join(self.output_dir, 'README.md')}")
        
        return self.output_dir

# ============================================================
# CLI INTERFACE
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Generate Interactive Courses")
    parser.add_argument("--topic", type=str, help="Course topic")
    parser.add_argument("--level", type=str, default="intermediate", 
                       choices=["beginner", "intermediate", "advanced"])
    parser.add_argument("--duration", type=str, default="full",
                       choices=["micro", "short", "full"])
    parser.add_argument("--format", type=str, default="both",
                       choices=["html", "markdown", "both"])
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    if args.interactive or not args.topic:
        print("\n=== Interactive Course Generator ===\n")
        topic = input("Enter course topic: ")
        level = input("Level (beginner/intermediate/advanced) [intermediate]: ") or "intermediate"
        duration = input("Duration (micro/short/full) [full]: ") or "full"
        fmt = input("Format (html/markdown/both) [both]: ") or "both"
    else:
        topic = args.topic
        level = args.level
        duration = args.duration
        fmt = args.format
    
    generator = CourseGenerator(topic, level, duration, fmt)
    generator.generate()

if __name__ == "__main__":
    main()
