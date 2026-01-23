"""
CrewAI Job Research - FREE VERSION
Uses Gemini API (zero cost) instead of OpenAI
No Serper needed - uses direct web research via Gemini
"""

from crewai import Agent, Task, Crew, Process, LLM
import json
import argparse
from pathlib import Path
from datetime import datetime
import os

# Gemini API keys (rotation)
GEMINI_KEYS = [
    "AIzaSyDuEcgiRLdx4UKNHvTJlF40CVMRmCVdVNA",
    "AIzaSyCef-lhv1Zlp0rmoQPFaCNR6lfkmAphEeU",
    "AIzaSyDrsYKTCsC9P5b20J-2E-3fe7EX5MA41Co",
    "AIzaSyBityHYy_f8dyT6iKwVxwhhls3cIvyPU1Q"
]

current_key_index = 0

def get_gemini_llm():
    """Get Gemini LLM configuration for CrewAI"""
    global current_key_index
    api_key = GEMINI_KEYS[current_key_index]
    
    # Create CrewAI LLM object for Gemini
    llm = LLM(
        model="gemini/gemini-1.5-flash",
        api_key=api_key
    )
    
    return llm

def create_job_research_crew():
    """Create specialized crew using FREE Gemini API"""
    
    # Get Gemini LLM
    llm = get_gemini_llm()
    
    # Agent 1: Company Intelligence Analyst (NO TOOLS - uses Gemini's knowledge)
    company_researcher = Agent(
        role='Company Intelligence Analyst',
        goal='Conduct deep research on company culture, projects, and values using your knowledge',
        backstory='''You are an expert corporate researcher with extensive knowledge of companies,
        industries, and market trends. You excel at analyzing company culture, recent projects,
        strategic direction, and employee experiences based on your training data and reasoning.
        You provide comprehensive insights without needing external tools.''',
        verbose=True,
        llm=llm,
        allow_delegation=False
    )
   
    # Agent 2: Job Requirements Analyst (NO TOOLS - uses reasoning)
    job_analyst = Agent(
        role='Job Requirements Analyst',
        goal='Extract and structure job requirements from descriptions',
        backstory='''You are an experienced recruiter who has reviewed thousands of job postings.
        You can identify must-have requirements versus nice-to-haves, understand implicit
        requirements, and recognize what companies really value based on how they write job
        descriptions. You use your expertise to analyze postings thoroughly.''',
        verbose=True,
        llm=llm,
        allow_delegation=False
    )
    
    # Agent 3: Application Strategy Advisor (NO TOOLS - uses expertise)
    strategist = Agent(
        role='Application Strategy Advisor',
        goal='Create winning application strategies based on research',
        backstory='''You are a career coach with a proven track record of helping candidates
        land jobs. You understand how to position candidates, address potential gaps, and
        emphasize relevant experience. You know what makes applications stand out and can
        create customized strategies without external data.''',
        verbose=True,
        llm=llm,
        allow_delegation=False
    )
    
    return {
        'company_researcher': company_researcher,
        'job_analyst': job_analyst,
        'strategist': strategist
    }

def create_research_tasks(agents, company, role, url):
    """Create research tasks"""
    
    # Task 1: Company Research
    research_company = Task(
        description=f'''Research {company} thoroughly based on your knowledge:

        1. Company overview and history
        2. Recent projects and industry presence
        3. Company values, mission, and culture (what you know about them)
        4. Market position and reputation
        5. Likely technology stack for a {role} role
        6. Company culture indicators
        
        Provide comprehensive insights based on what you know about {company}.
        Reference URL for context: {url}
        ''',
        expected_output='''Comprehensive company intelligence report including:
        - Company overview and background
        - Culture assessment based on industry knowledge
        - Technology and tools likely used
        - Key opportunities and challenges
        - Actionable insights for job applicants''',
        agent=agents['company_researcher']
    )
    
    # Task 2: Job Posting Analysis
    analyze_job = Task(
        description=f'''Analyze what a {role} position at {company} would typically require:
        
        1. Standard must-have requirements for this role
        2. Likely nice-to-have qualifications
        3. Typical key responsibilities for {role}
        4. Expected success metrics
        5. Seniority level analysis
        6. Growth opportunities for this role
        
        Base your analysis on industry standards and {company}'s profile.
        Job URL for reference: {url}
        ''',
        expected_output='''Structured job analysis including:
        - Critical requirements (must-have)
        - Preferred qualifications (nice-to-have)
        - Core responsibilities
        - Success indicators
        - Hidden requirements or expectations
        - Career growth potential''',
        agent=agents['job_analyst'],
        context=[research_company]
    )
    
    # Task 3: Application Strategy
    create_strategy = Task(
        description=f'''Create a tailored application strategy for {role} at {company}:
        
        Based on the company research and job analysis, determine:
        1. Key points to emphasize in application
        2. How to frame project controls/planning experience
        3. Skills to highlight most prominently
        4. Potential concerns to address proactively
        5. Unique value proposition angle
        6. Cover letter focus areas
        7. Interview preparation insights
        
        Consider that the candidate has:
        - Project controls and planning experience
        - Primavera P6 expertise
        - International project experience
        - Strong analytical skills
        ''',
        expected_output='''Application strategy document including:
        - Top 5 points to emphasize
        - Experience framing recommendations
        - Skills priority ranking
        - Gap mitigation strategies
        - Unique positioning angle
        - Cover letter outline
        - Interview preparation tips''',
        agent=agents['strategist'],
        context=[research_company, analyze_job]
    )
    
    return [research_company, analyze_job, create_strategy]

def run_job_research(company, role, url, output_dir='data'):
    """Execute job research crew with FREE Gemini"""
    
    print(f"\n{'='*60}")
    print(f"🤖 CrewAI Job Research (FREE - Gemini API)")
    print(f"{'='*60}")
    print(f"Company: {company}")
    print(f"Role: {role}")
    print(f"URL: {url}")
    print(f"{'='*60}\n")
    
    # Create agents
    agents = create_job_research_crew()
    
    # Create tasks
    tasks = create_research_tasks(agents, company, role, url)
    
    # Create crew
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    # Execute
    print("\n🔄 Starting research with Gemini AI...\n")
    result = crew.kickoff()
    
    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_company = company.replace(' ', '_').replace('/', '_')
    
    output_file = output_path / f"crewai_research_{safe_company}_{timestamp}.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Job Research Report (Gemini AI)\n\n")
        f.write(f"**Company**: {company}\n")
        f.write(f"**Role**: {role}\n")
        f.write(f"**URL**: {url}\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        f.write(str(result))
    
    print(f"\n{'='*60}")
    print(f"✅ Research Complete!")
    print(f"📁 Saved to: {output_file}")
    print(f"{'='*60}\n")
    
    return result, output_file

def research_from_gemini_results(gemini_json_path):
    """Research all jobs from Gemini search results"""
    
    # Load Gemini results
    with open(gemini_json_path, 'r', encoding='utf-8') as f:
        jobs = json.load(f)
    
    print(f"\n📋 Found {len(jobs)} jobs in Gemini results")
    print(f"💡 Using FREE Gemini API for all research\n")
    
    results = []
    for idx, job in enumerate(jobs, 1):
        print(f"\n{'='*60}")
        print(f"Processing Job {idx}/{len(jobs)}")
        print(f"{'='*60}")
        
        try:
            result, output_file = run_job_research(
                company=job['company'],
                role=job['title'],
                url=job['url'],
                output_dir='job-application/data'
            )
            
            results.append({
                'job': job,
                'research_file': str(output_file),
                'status': 'success'
            })
        except Exception as e:
            print(f"\n❌ Error processing {job['company']}: {e}")
            results.append({
                'job': job,
                'status': 'failed',
                'error': str(e)
            })
    
    # Save index
    index_file = Path('job-application/data/crewai_research_index.json')
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    successful = sum(1 for r in results if r.get('status') == 'success')
    print(f"\n✅ All research complete!")
    print(f"📊 Successful: {successful}/{len(jobs)}")
    print(f"📊 Index saved to: {index_file}")
    
    return results

def main():
    parser = argparse.ArgumentParser(
        description='CrewAI Job Research - FREE version with Gemini AI'
    )
    
    parser.add_argument('--company', help='Company name')
    parser.add_argument('--role', help='Job role/title')
    parser.add_argument('--url', help='Job posting URL')
    parser.add_argument('--input', help='Path to gemini_jobs.json for batch processing')
    parser.add_argument('--output-dir', default='job-application/data', 
                       help='Output directory for research reports')
    
    args = parser.parse_args()
    
    print("\n💰 FREE VERSION - Using Gemini API (zero cost)")
    print("=" * 60)
    
    try:
        if args.input:
            # Batch process from Gemini results
            research_from_gemini_results(args.input)
        elif args.company and args.role and args.url:
            # Single job research
            run_job_research(args.company, args.role, args.url, args.output_dir)
        else:
            # Interactive mode
            print("\n🤖 CrewAI Job Research - Interactive Mode\n")
            company = input("Company name: ")
            role = input("Job role/title: ")
            url = input("Job posting URL: ")
            
            run_job_research(company, role, url, args.output_dir)
            
    except KeyboardInterrupt:
        print("\n\n❌ Research cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
