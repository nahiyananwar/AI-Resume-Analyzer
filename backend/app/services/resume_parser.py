"""
Resume Parser Service
Extracts key information from resume text using spaCy NER and regex
"""
import re
import spacy
from typing import List, Optional, Tuple
from datetime import datetime
from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta


# Load spaCy model - installed via requirements.txt
nlp = spacy.load("en_core_web_sm")


# Common skills list for extraction
COMMON_SKILLS = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "go", "golang",
    "rust", "php", "swift", "kotlin", "scala", "r", "matlab", "perl", "bash", "shell",
    
    # Web Technologies
    "html", "css", "sass", "less", "react", "reactjs", "react.js", "angular", "angularjs",
    "vue", "vuejs", "vue.js", "next.js", "nextjs", "nuxt", "svelte", "jquery", "bootstrap",
    "tailwind", "tailwindcss", "material-ui", "webpack", "vite", "node.js", "nodejs",
    "express", "expressjs", "fastapi", "flask", "django", "spring", "spring boot",
    "asp.net", ".net", "graphql", "rest", "restful", "api",
    
    # Databases
    "sql", "mysql", "postgresql", "postgres", "mongodb", "redis", "elasticsearch",
    "cassandra", "dynamodb", "sqlite", "oracle", "sql server", "mariadb", "firebase",
    
    # Cloud & DevOps
    "aws", "amazon web services", "azure", "gcp", "google cloud", "docker", "kubernetes",
    "k8s", "jenkins", "ci/cd", "terraform", "ansible", "puppet", "chef", "nginx",
    "apache", "linux", "unix", "git", "github", "gitlab", "bitbucket", "jira",
    
    # AI/ML
    "machine learning", "deep learning", "tensorflow", "pytorch", "keras", "scikit-learn",
    "sklearn", "pandas", "numpy", "scipy", "matplotlib", "seaborn", "opencv", "nlp",
    "natural language processing", "computer vision", "neural networks", "cnn", "rnn",
    "lstm", "transformer", "bert", "gpt", "hugging face", "langchain", "llm",
    
    # Data
    "data analysis", "data science", "data engineering", "etl", "data visualization",
    "tableau", "power bi", "looker", "airflow", "spark", "hadoop", "hive", "kafka",
    "big data", "data mining", "statistics", "a/b testing",
    
    # Other
    "agile", "scrum", "kanban", "microservices", "oop", "design patterns", "tdd",
    "unit testing", "integration testing", "selenium", "cypress", "jest", "pytest",
    "security", "oauth", "jwt", "ssl", "https"
]


def extract_email(text: str) -> Optional[str]:
    """Extract email address from text using regex"""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else None


def extract_phone(text: str) -> Optional[str]:
    """Extract phone number from text using regex"""
    # Multiple patterns to catch different phone formats
    patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # +1 (123) 456-7890
        r'\+?\d{1,3}[-.\s]?\d{2,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}',  # International
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (123) 456-7890
        r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # 123-456-7890
        r'\d{10,11}',  # 1234567890
        r'0\d{2}[-.\s]?\d{4}[-.\s]?\d{4}',  # 017-1234-5678 (BD format)
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            # Clean up the phone number
            phone = matches[0].strip()
            # Remove extra whitespace
            phone = re.sub(r'\s+', ' ', phone)
            return phone
    
    return None


def extract_name(text: str) -> Optional[str]:
    """Extract name from text - prioritizing first lines where names typically appear"""
    lines = text.split('\n')
    
    # Common non-name headers/sections to skip
    skip_patterns = [
        r'^(resume|cv|curriculum\s*vitae|profile|about|summary|objective|contact|experience|education|skills|projects|work|professional)s?$',
        r'^(email|phone|address|linkedin|github|portfolio|website)s?:?$',
        r'^(mr|ms|mrs|dr|prof)\.?\s*$',
        r'^\d+',  # Starts with digit
        r'^[+\(\d]',  # Phone number patterns
        r'@',  # Email
        r'^http',  # URLs
        r'^www\.',  # URLs
    ]
    
    # First pass: Check first 5 non-empty lines for a name-like pattern
    checked = 0
    for line in lines:
        if checked >= 5:
            break
            
        line = line.strip()
        if not line or len(line) < 3:
            continue
            
        checked += 1
        line_lower = line.lower()
        
        # Skip if matches a skip pattern
        should_skip = False
        for pattern in skip_patterns:
            if re.search(pattern, line_lower, re.IGNORECASE):
                should_skip = True
                break
        if should_skip:
            continue
        
        # Check if line looks like a name:
        # - 2-5 words
        # - Only letters, spaces, dots, hyphens, apostrophes
        # - No digits
        # - Not too long (names usually under 50 chars)
        words = line.split()
        if 2 <= len(words) <= 5 and len(line) < 50:
            # Allow: letters, spaces, dots, hyphens, apostrophes
            if re.match(r"^[A-Za-z][A-Za-z\s.\-']+$", line):
                # Additional check: not all uppercase (likely a header)
                if not line.isupper() or len(words) <= 3:
                    # Capitalize properly
                    return ' '.join(word.capitalize() if word.islower() else word for word in words)
    
    # Second pass: Use spaCy NER on first portion
    first_portion = text[:1500] if len(text) > 1500 else text
    doc = nlp(first_portion)
    
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text.strip()
            # Validate: at least 2 chars, no digits, not all symbols
            if len(name) >= 2 and not re.search(r'\d', name) and not re.match(r'^[\W]+$', name):
                # Check it's not a common non-name word
                name_lower = name.lower()
                if not any(re.search(p, name_lower) for p in skip_patterns):
                    return name
    
    # Third pass: Relaxed check on first 10 lines
    for line in lines[:10]:
        line = line.strip()
        if not line:
            continue
        words = line.split()
        # Accept 2-4 word lines that look like names
        if 2 <= len(words) <= 4 and len(line) < 40:
            if re.match(r"^[A-Za-z][A-Za-z\s.\-']+$", line):
                # Skip if likely a section header
                line_lower = line.lower()
                if not any(kw in line_lower for kw in ['experience', 'education', 'skill', 'project', 'work', 'summary', 'objective', 'contact']):
                    return ' '.join(word.capitalize() if word.islower() else word for word in words)
    
    return None


def extract_skills(text: str) -> List[str]:
    """Extract skills from text by matching against common skills list"""
    text_lower = text.lower()
    found_skills = []
    
    for skill in COMMON_SKILLS:
        # Use word boundaries to match whole words
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            # Capitalize properly
            if skill.isupper() or skill in ['aws', 'gcp', 'sql', 'html', 'css', 'php', 'api', 'llm', 'nlp', 'cnn', 'rnn', 'lstm', 'jwt', 'ssl', 'https', 'tdd', 'oop', 'k8s']:
                found_skills.append(skill.upper())
            elif '.' in skill or '-' in skill:
                found_skills.append(skill)
            else:
                found_skills.append(skill.title())
    
    # Remove duplicates while preserving order
    seen = set()
    unique_skills = []
    for skill in found_skills:
        skill_lower = skill.lower()
        if skill_lower not in seen:
            seen.add(skill_lower)
            unique_skills.append(skill)
    
    return unique_skills[:30]  # Limit to top 30 skills


def extract_education(text: str) -> List[str]:
    """Extract education information from text"""
    education_keywords = [
        r"\bbachelor'?s?\b", r"\bmaster'?s?\b", r"\bph\.?d\.?\b", r"\bdoctorate\b", r"\bdiploma\b",
        r"\bb\.?s\.?c?\.?\b", r"\bm\.?s\.?c?\.?\b", r"\bb\.?a\.?\b", r"\bm\.?a\.?\b", r"\bb\.?e\.?\b",
        r"\bm\.?e\.?\b", r"\bb\.?tech\b", r"\bm\.?tech\b", r"\bmba\b", r"\bbba\b",
        r"\bassociate'?s?\s+degree\b", r"\bcertificate\b", r"\bcertification\b",
        r"\bssc\b", r"\bhsc\b", r"\ba\s*[-]?levels?\b", r"\bo\s*[-]?levels?\b"
    ]
    
    degree_pattern = '|'.join(education_keywords)
    
    # Also look for university/college mentions
    # Support both "University of X" and "X University"
    institution_pattern = r'(?:university|college|institute|school)\s+(?:of\s+)?[A-Za-z\s]+|[A-Za-z\s]+\s+(?:university|college|institute|school)'
    
    lines = text.split('\n')
    education_entries = []
    skip_indices = set()
    
    # Regex for checking if a line is primarily a date/year
    # Matches: "2020", "Jan 2020", "2020-2024", "December 2024", "Present", etc.
    date_line_pattern = r'\b((?:19|20)\d{2}|present|current|now|ongoing|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b'
    
    for i, line in enumerate(lines):
        if i in skip_indices:
            continue
            
        line = line.strip()
        if not line:
            continue
            
        # Skip lines that verify as emails or URLs
        if '@' in line or 'http' in line or 'www.' in line or '.com' in line:
            continue
            
        # Skip lines that look like headers or skill lists
        if len(line.split()) == 1 and re.match(degree_pattern, line, re.IGNORECASE):
             continue

        if ':' in line and not ('GPA' in line or 'Grade' in line):
            # unlikely to be an education line if it has a colon but no GPA
            continue
            
        # Skip lines that look like Job Titles or Project Roles
        # "Team Leader", "Project", "Intern", "Coordinator" etc. should be filtered unless they have a strong degree
        if re.search(r'\b(manager|professor|assistant|lead|senior|junior|intern|member|coordinator|volunteer|developer|engineer)\b', line, re.IGNORECASE) or \
           re.search(r'\b(project|research|work|experience)\b', line, re.IGNORECASE):
             strong_degrees = r"\b(bachelor|master|ph\.?d|doctorate|b\.?sc|m\.?sc|mba|ssc|hsc|levels?)\b"
             if not re.search(strong_degrees, line, re.IGNORECASE):
                 # If it doesn't have a strong degree, it's likely experience/project
                 continue

        # Check for deduplication
        dup_match = re.match(r'^(.+?)\s+\1$', line, re.IGNORECASE)
        if dup_match and len(dup_match.group(1)) > 5:
            line = dup_match.group(1).strip()

        # Check if line contains education keywords
        if re.search(degree_pattern, line, re.IGNORECASE):
            # Try to capture context (Date/University) from adjacent lines if they look like dates OR institutions
            
            # Check PREVIOUS line for Date/Institution
            if i > 0:
                prev_line = lines[i-1].strip()
                # If prev line is date or institution
                is_date = len(prev_line) < 30 and re.search(date_line_pattern, prev_line, re.IGNORECASE)
                is_inst = len(prev_line) < 100 and re.search(institution_pattern, prev_line, re.IGNORECASE)
                
                if (is_date or is_inst) and "project" not in prev_line.lower(): # Avoid merging project lines
                     line = prev_line + " " + line
            
            # Check NEXT line for Date/Institution
            if i < len(lines) - 1 and (i+1) not in skip_indices:
                next_line = lines[i+1].strip()
                is_date = len(next_line) < 30 and re.search(date_line_pattern, next_line, re.IGNORECASE)
                is_inst = len(next_line) < 100 and re.search(institution_pattern, next_line, re.IGNORECASE)
                
                # Double check deduplication on next line too
                dup_match_next = re.match(r'^(.+?)\s+\1$', next_line, re.IGNORECASE)
                if dup_match_next and len(dup_match_next.group(1)) > 5:
                    next_line = dup_match_next.group(1).strip()
                
                if (is_date or is_inst) and "project" not in next_line.lower():
                     line = line + ", " + next_line
                     skip_indices.add(i+1)

            # Clean up the line
            if len(line) < 400:  # Allow longer for merged lines
                education_entries.append(line)
                continue
    
    # Remove duplicates and fuzzy subsets
    
    # Remove duplicates and fuzzy subsets
    # Logic: If 'North South University' is in the list, but we also have 'B.Sc ... North South University',
    # remove the shorter one.
    
    # 1. Sort by length descending (longest first)
    # 2. Keep entry if it isn't contained in any already-kept entry
    
    seen = set()
    unique_education = []
    
    # First pass: simple deduplication
    temp_unique = []
    for entry in education_entries:
        entry_lower = entry.lower()
        if entry_lower not in seen:
            seen.add(entry_lower)
            temp_unique.append(entry)
            
    # Second pass: substring filtering
    # Sort by length descending
    temp_unique.sort(key=len, reverse=True)
    
    final_education = []
    for entry in temp_unique:
        is_contained = False
        for kept in final_education:
            # Check if current entry is a substring of an existing (longer) kept entry
            # normalize punctuation/spacing? simple strict string check usually works for exact substrings
            # "North South University" in "B.Sc ... North South University"
            if entry in kept:
                is_contained = True
                break
        
        if not is_contained:
            final_education.append(entry)
    
    return final_education[:5]  # Limit to 5 entries


def parse_date(date_str: str) -> Optional[datetime]:
    """Parse a date string into a datetime object"""
    date_str = date_str.strip().lower()
    
    # Handle "present", "current", "now"
    if date_str in ['present', 'current', 'now', 'ongoing', 'till date', 'to date']:
        return datetime.now()
    
    try:
        return date_parser.parse(date_str, fuzzy=True)
    except:
        pass
    
    # Try year only
    year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
    if year_match:
        try:
            return datetime(int(year_match.group()), 6, 1)  # Assume middle of year
        except:
            pass
    
    return None


def extract_experience_details(text: str) -> Tuple[float, List[dict]]:
    """
    extract total years and a breakdown of experience by role
    Returns: (total_years, breakdown_list)
    breakdown_list = [{"title": str, "years": float, "is_current": bool}]
    """
    # Patterns for date ranges
    date_range_patterns = [
        # "Jan 2020 - Present", "January 2020 to December 2023"
        r'((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*\d{4})\s*[-–—to]+\s*((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*\d{4}|present|current|now|ongoing)',
        # "2020 - 2023", "2020-Present"
        r'(\b(?:19|20)\d{2}\b)\s*[-–—to]+\s*((?:19|20)\d{2}|present|current|now|ongoing)',
        # "03/2020 - 12/2023"
        r'(\d{1,2}/\d{4})\s*[-–—to]+\s*(\d{1,2}/\d{4}|present|current|now|ongoing)',
    ]
    
    total_months = 0
    breakdown = []
    
    # Common job titles to look for
    # We will search context around dates for these
    job_keywords = [
        "developer", "engineer", "scientist", "analyst", "manager", "lead", "architect", 
        "consultant", "administrator", "designer", "intern", "assistant", "executive", 
        "officer", "representative", "specialist", "coordinator", "director", "head",
        "vp", "president", "founder", "co-founder", "support", "service", "agent"
    ]
    
    lines = text.split('\n')
    text_lower = text.lower()
    
    # Helper to find title in context
    def find_title_in_context(line_idx, lines_list):
        # Check current line, 2 lines before, AND 2 lines after
        # Many resumes have Date \n Title or Title \n Date
        start = max(0, line_idx - 2)
        end = min(len(lines_list), line_idx + 3) # +3 to include line_idx+2
        context = lines_list[start:end]
        
        best_title = "Unknown Role"
        for l in context:
            l = l.strip()
            if not l: continue
            
            # Simple check: does it contain a known role keyword?
            for kw in job_keywords:
                 if re.search(r'\b' + re.escape(kw) + r'\b', l, re.IGNORECASE):
                      # Avoid "Project Manager" if we only matched "Manager"? No, keep generic.
                      # Ideally we want the full title.
                      # Let's clean the line and use it if it's not too long
                      if len(l) < 80: # Increased limit to capture longer titles
                          return l
        return best_title

    # We need to match date ranges in the original text structure (lines)
    # But regex finds them in the whole string.
    # Let's iterate lines and find date ranges line by line to keep context.
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        for pattern in date_range_patterns:
            matches = re.findall(pattern, line_lower, re.IGNORECASE)
            for match in matches:
                start_str, end_str = match
                start_date = parse_date(start_str)
                end_date = parse_date(end_str)
                
                if start_date and end_date:
                    # Calculate months
                    if end_date > start_date:
                        diff = relativedelta(end_date, start_date)
                        months = diff.years * 12 + diff.months
                        if months > 0:
                            # Contextualize
                            title = find_title_in_context(i, lines)
                            
                            breakdown.append({
                                "title": title,
                                "years": round(months / 12.0, 1),
                                "start": start_str,
                                "end": end_str
                            })
                            total_months += months

    # Deduplicate breakdown: If same title and almost same years, probably duplicate find
    # Or if overlap. For now simple summary.
    
    # If no date ranges found, fallback to total years logic (without breakdown)
    if total_months == 0:
        # "5 years of experience"
        exp_patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(?:experience|exp)[:\s]*(\d+)\+?\s*(?:years?|yrs?)',
             r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:in|of|as)',
        ]
        total_yrs = 0.0
        for pattern in exp_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                try:
                    total_yrs = max(float(m) for m in matches)
                except:
                    pass
        return total_yrs, []

    # Convert months to years
    years = total_months / 12.0
    return round(years, 1), breakdown

def extract_experience_years(text: str) -> float:
    # Wrapper for backward compatibility if needed, but we will use the new one usually
    y, _ = extract_experience_details(text)
    return y


def get_experience_level(years: float) -> str:
    """Determine experience level based on years of experience"""
    if years < 2:
        return "Junior"
    elif years < 5:
        return "Mid"
    else:
        return "Senior"


def parse_resume(text: str) -> dict:
    """
    Parse resume text and extract all relevant information
    
    Args:
        text: Resume text content
        
    Returns:
        Dictionary with extracted information
    """
    exp_years, exp_breakdown = extract_experience_details(text)
    
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience_years": exp_years,
        "experience_breakdown": exp_breakdown
    }
