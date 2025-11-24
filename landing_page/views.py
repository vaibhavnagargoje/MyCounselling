from django.shortcuts import render
from django.http import Http404
from django.urls import reverse

COLLEGE_DATA = [
    {
        "id": 1,
        "code": "DYPCOE",
        "name": "Dr. D. Y. Patil College of Engineering, Pune",
        "accreditation": "NAAC A+ · NBA Accredited",
        "status": "Autonomous · AICTE Approved",
        "location": "Pune, Maharashtra",
        "rankings": [
            "NIRF 2023 Engineering: 72",
            "Times Top Private: 18"
        ],
        "specialisations": ["CSE", "AI & DS", "ENTC", "Mechanical"],
        "contact": {
            "email": "admissions@dypcoe.edu",
            "phone": "+91-2023-456-789",
            "website": "https://www.dypcoe.edu",
            "address": "Sector 29, Nigdi, Pune 411044"
        },
        "placement": {
            "academic_year": "2023-24",
            "placement_percentage": 93,
            "students_placed": 612,
            "total_students": 658,
            "highest_package": 36.5,
            "average_package": 9.2,
            "top_recruiters": ["Amazon", "TCS Digital", "Airtel", "Dassault"],
            "notable_projects": [
                "EV powertrain research lab",
                "AI-driven counselling chatbot"
            ]
        }
    },
    {
        "id": 2,
        "code": "VITPUNE",
        "name": "Vishwakarma Institute of Technology, Pune",
        "accreditation": "NAAC A++ · NBA Tier-1",
        "status": "Deemed · UGC Autonomous",
        "location": "Bibvewadi, Pune",
        "rankings": [
            "NIRF 2023 Engineering: 82",
            "India Today Private: 14"
        ],
        "specialisations": ["CSE", "IT", "Chemical", "Robotics"],
        "contact": {
            "email": "info@vit.edu",
            "phone": "+91-2024-567-890",
            "website": "https://www.vit.edu",
            "address": "666, Upper Indira Nagar, Pune 411037"
        },
        "placement": {
            "academic_year": "2023-24",
            "placement_percentage": 96,
            "students_placed": 702,
            "total_students": 730,
            "highest_package": 45.0,
            "average_package": 11.4,
            "top_recruiters": ["Google", "Mercedes-Benz", "PwC", "Cognizant"],
            "notable_projects": [
                "Autonomous vehicle lab",
                "Smart campus energy grid"
            ]
        }
    },
    {
        "id": 3,
        "code": "KLETECH",
        "name": "KLE Technological University, Hubballi",
        "accreditation": "NAAC A · NBA",
        "status": "State Private University",
        "location": "Hubballi, Karnataka",
        "rankings": [
            "NIRF 2023 Engineering: 101-150 band",
            "ARIIA Innovation Rank: 6"
        ],
        "specialisations": ["EEE", "Civil", "CSE", "Bio-Tech"],
        "contact": {
            "email": "admissions@kletech.ac.in",
            "phone": "+91-8362-372-700",
            "website": "https://www.kletech.ac.in",
            "address": "Vidyanagar, Hubballi 580031"
        },
        "placement": {
            "academic_year": "2023-24",
            "placement_percentage": 88,
            "students_placed": 502,
            "total_students": 570,
            "highest_package": 28.4,
            "average_package": 7.6,
            "top_recruiters": ["Siemens", "L&T", "Infosys", "Bosch"],
            "notable_projects": [
                "Smart irrigation IoT cluster",
                "Rural entrepreneurship hub"
            ]
        }
    }
]

CAREER_STATS = [
    {"value": "50K+", "label": "Students Served"},
    {"value": "120+", "label": "Employees"},
    {"value": "12", "label": "Cities"},
    {"value": "4.8/5", "label": "Glassdoor Score"},
]

CAREER_BENEFITS = [
    {"icon": "fas fa-lightbulb", "title": "Mission-first culture", "desc": "We’re obsessed with helping students make confident admission decisions."},
    {"icon": "fas fa-user-graduate", "title": "Learning stipend", "desc": "Dedicated budget for certifications, conferences, and mentorship."},
    {"icon": "fas fa-heart", "title": "Wellness benefits", "desc": "Comprehensive health cover, counselling credits, remote-friendly policies."},
    {"icon": "fas fa-globe", "title": "Hybrid work", "desc": "Choose Pune HQ, regional hubs, or remote roles with travel support."},
    {"icon": "fas fa-chart-line", "title": "Stock options", "desc": "ESOPs for core team members across functions."},
    {"icon": "fas fa-hands-helping", "title": "Inclusive teams", "desc": "50% women leadership, mentors from Tier-2/3 cities, no degree bias."},
]

CAREER_ROLES = [
    {
        "title": "Senior Product Designer",
        "team": "Design · Pune/Remote",
        "tags": ["Figma", "Design Systems", "Motion"],
        "summary": "Own end-to-end UX for student dashboards and counsellor workflows."
    },
    {
        "title": "Counselling Lead – Medical",
        "team": "Operations · Mumbai/Pune",
        "tags": ["NEET", "Team Management", "Student Success"],
        "summary": "Coach 25+ counsellors, run mock allotments, and publish city-level reports."
    },
    {
        "title": "Data Scientist – Predictors",
        "team": "Data & AI · Remote",
        "tags": ["Python", "Time-series", "ML Ops"],
        "summary": "Improve rank/college prediction accuracy using seat matrix & behaviour data."
    },
    {
        "title": "Growth Marketing Manager",
        "team": "Marketing · Bengaluru",
        "tags": ["Lifecycle", "Paid Media", "Automation"],
        "summary": "Own acquisition funnels, webinars, and partner campaigns."
    },
]

FEATURED_TOOLS = [
    {
        "title": "College Predictor",
        "desc": "Personalized college lists mapped to your rank, budget, and preferred states.",
        "badge": "Free Tool",
        "icon_class": "fas fa-university",
        "gradient": "bg-gradient-to-r from-blue-500 to-blue-600",
        "url_name": "college_predictor",
    },
    {
        "title": "Rank Predictor",
        "desc": "AI-assisted rank estimates with live difficulty calibration and historical trends.",
        "badge": "Free Tool",
        "icon_class": "fas fa-calculator",
        "gradient": "bg-gradient-to-r from-purple-500 to-purple-600",
        "url_name": "rankpredictor",
    },
    {
        "title": "College Database",
        "desc": "Curated repository of 2500+ institutes with fees, cut-offs, and placement stats.",
        "badge": "Premium",
        "icon_class": "fas fa-database",
        "gradient": "bg-gradient-to-r from-green-500 to-green-600",
        "url_name": "colleges",
    },
]

PRO_SERVICES = [
    {
        "title": "1:1 Counselling Pods",
        "tier": "Premium",
        "icon": "fas fa-user-tie",
        "desc": "Dedicated mentor till seat locking with weekly war-room calls.",
        "highlights": [
            "Choice-filling rehearsals",
            "Seat tracker & escalation desk",
            "Parent updates every Friday",
        ],
        "cta": "Book Mentor Call",
        "url_name": "contact",
    },
    {
        "title": "Exam Rank Recovery Sprint",
        "tier": "Free Add-on",
        "icon": "fas fa-chart-line",
        "desc": "Pair Rank Predictor insights with live analytics to recalibrate targets.",
        "highlights": [
            "Rank Predictor sync",
            "Gap analysis playbook",
            "Upgrade-ready insights",
        ],
        "cta": "Launch Rank Predictor",
        "url_name": "rankpredictor",
    },
    {
        "title": "College Research Desk",
        "tier": "Elite",
        "icon": "fas fa-university",
        "desc": "Deep dives into our college database with mentor-led office hours.",
        "highlights": [
            "2500+ verified colleges",
            "Cut-off · fees · placement cards",
            "Ask-us-anything threads",
        ],
        "cta": "Browse Colleges",
        "url_name": "colleges",
    },
]

WORKFLOW_STEPS = [
    {"title": "Diagnostic Call", "desc": "Understand profile, ranks, preferences, and constraints."},
    {"title": "Data-backed Plan", "desc": "Deliver predictor output, shortlist, and funding pathways."},
    {"title": "Guided Execution", "desc": "Choice filling rehearsals, document vault, and round tracking."},
    {"title": "Seat Acceptance", "desc": "Post-seat onboarding, hostel help, and alumni connects."},
]

FAQS = [
    {"q": "How accurate are the predictors?", "a": "Powered by 6 years of counselling data, live exam-difficulty signals, and mentor overrides."},
    {"q": "Can I upgrade plans mid-way?", "a": "Yes, pay the difference anytime to unlock Pro or Elite services instantly."},
    {"q": "Do you support multiple exams?", "a": "Single dashboard handles NEET, JEE, CET, COMEDK, VITEEE, and state rounds together."},
]

# Create your views here.

def index(request):
    # if request.user.is_authenticated:
    #     return render(request, 'home/home.html')
    return render(request, 'landing_page/index.html')



def colleges(request):
    return render(request, 'landing_page/colleges.html', {"colleges": COLLEGE_DATA})

def college_details(request, college_id):
    college = next((c for c in COLLEGE_DATA if c["id"] == college_id), None)
    if college is None:
        raise Http404("College not found")
    return render(request, 'landing_page/college-details.html', {"college": college})


def about_us(request):
    return render(request, 'landing_page/about-us.html')

def careers(request):
    context = {
        "career_stats": CAREER_STATS,
        "career_benefits": CAREER_BENEFITS,
        "career_roles": CAREER_ROLES,
    }
    return render(request,'landing_page/careers.html', context)

def tools_and_services(request):
    
    
    return render(request, 'landing_page/tools-and-services.html')

def contact(request):
    return render(request, 'landing_page/contact.html')