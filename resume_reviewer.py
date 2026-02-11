import sys
import os
import argparse
# import pypdf # Need to install: pip install pypdf

def extract_text_from_pdf(pdf_path):
    """Placeholder for PDF text extraction."""
    print(f"Extracting text from {pdf_path}...")
    # TODO: Implement pypdf logic
    return "Sample Resume Text"

def critique_resume(resume_text, job_description=""):
    """Placeholder for LLM critique logic."""
    print("Analyzing resume against best practices...")
    
    critique = []
    critique.append("- Strong action verbs missing in bullet points 2 & 3.")
    critique.append("- Quantify results! 'Managed project' -> 'Managed $50k project'.")
    
    if job_description:
        print(f"Comparing against job description...")
        critique.append("- Missing keyword: 'Python' (mentioned in JD).")
        
    return "\n".join(critique)

def main():
    parser = argparse.ArgumentParser(description="AI Resume Reviewer")
    parser.add_argument("resume_path", help="Path to PDF resume")
    parser.add_argument("--job", help="Path to Job Description (txt file)", default="")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.resume_path):
        print(f"Error: Resume not found at {args.resume_path}")
        return

    text = extract_text_from_pdf(args.resume_path)
    
    jd_text = ""
    if args.job and os.path.exists(args.job):
        with open(args.job, 'r') as f:
            jd_text = f.read()
            
    feedback = critique_resume(text, jd_text)
    
    print("\n--- RESUME CRITIQUE ---\n")
    print(feedback)
    print("\n-----------------------")

if __name__ == "__main__":
    main()