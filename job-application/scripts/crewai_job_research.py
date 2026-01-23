"""
CrewAI Job Research Integration
Deep company and role research using multi-agent system
"""

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, WebsiteSearchTool
import json
import argparse
from pathlib import Path
from datetime import datetime

def create_job_research_crew():
    """Create specialized crew for job application research"""
    
    # Initialize tools
    search_tool = SerperDevTool()
    website_tool = WebsiteSearchTool()
    
    # Agent 1: Company Intelligence Analyst
    company_researcher = Agent(
        role='Company Intelligence Analyst',
        goal='Conduct deep research on company culture, projects, and values',
        backstory='''You are an expert corporate researcher with access to multiple 
        data sources. You excel at uncovering insights about company culture, recent 
        projects, strategic direction, and employee experiences. You know how to read 
        between the lines of public information.''',
        verbose=True,
        tools=[search_tool, website_tool],
        allow_delegation=False
    )
   
    # Agent 2: Job Requirements Analyst
    job_analyst = Agent(
        role='Job Requirements Analyst',
        goal='Extract and structure job requirements from postings',
        backstory='''You are an experienced recruiter who has reviewed thousands 
        of job postings. You can identify must-have requirements versus nice-to-haves, 
        understand implicit requirements, and recognize what companies really value 
        based on how they write job descriptions.''',
        verbose=True,
        tools=[website_tool],
        allow_delegation=False
    )
    
    # Agent 3: Application Strategy Advisor
    strategist = Agent(
        role='Application Strategy Advisor',
        goal='Create winning application strategies based on research',
        backstory='''You are a career coach with a proven track record of helping 
        candidates land jobs. You understand how to position candidates, address 
        potential gaps, and emphasize relevant experience. You know what makes 
        applications stand out.''',
        verbose=True,
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
        description=f'''Research {company} thoroughly:

        1. Recent projects and news (last 6 months)
        2. Company values, mission, and culture
        3. Growth trajectory and market position
        4. Employee reviews and workplace culture signals
        5. Technology stack and tools they use
        6. Notable achievements or awards
        
        Focus on information relevant to a {role} position.
        Company website: {url}
        ''',
        expected_output='''Comprehensive company intelligence report including:
        - Company overview and recent developments
        - Culture assessment
        - Technology and tools insights
        - Key opportunities and challenges
        - Actionable insights for job applicants''',
        agent=agents['company_researcher']
    )
    
    # Task 2: Job Posting Analysis
    analyze_job = Task(
        description=f'''Analyze the job posting for {role} at {company}:
        
        1. Extract must-have vs nice-to-have requirements
        2. Identify key responsibilities
        3. Determine success metrics mentioned
        4. Read between the lines for implicit requirements
        5. Assess seniority level and scope
        6. Identify growth opportunities in the role
        
        Job URL: {url}
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
        2. How to frame relevant experience
        3. Skills to highlight most prominently
        4. Potential concerns to address proactively
        5. Unique value proposition angle
        6. Cover letter focus areas
        7. Interview preparation insights
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
    """Execute job research crew"""
    
    print(f"\n{'='*60}")
    print(f"🤖 CrewAI Job Research")
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
    print("\n🔄 Starting research...\n")
    result = crew.kickoff()
    
    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_company = company.replace(' ', '_').replace('/', '_')
    
    output_file = output_path / f"crewai_research_{safe_company}_{timestamp}.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Job Research Report\n\n")
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
    
    results = []
    for idx, job in enumerate(jobs, 1):
        print(f"\n{'='*60}")
        print(f"Processing Job {idx}/{len(jobs)}")
        print(f"{'='*60}")
        
        result, output_file = run_job_research(
            company=job['company'],
            role=job['title'],
            url=job['url']
        )
        
        results.append({
            'job': job,
            'research_file': str(output_file)
        })
    
    # Save index
    index_file = Path('data/crewai_research_index.json')
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ All research complete!")
    print(f"📊 Index saved to: {index_file}")
    
    return results

def main():
    parser = argparse.ArgumentParser(
        description='CrewAI Job Research - Deep company and role analysis'
    )
    
    parser.add_argument('--company', help='Company name')
    parser.add_argument('--role', help='Job role/title')
    parser.add_argument('--url', help='Job posting URL')
    parser.add_argument('--input', help='Path to gemini_jobs.json for batch processing')
    parser.add_argument('--output-dir', default='job-application/data', 
                       help='Output directory for research reports')
    
    args = parser.parse_args()
    
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
