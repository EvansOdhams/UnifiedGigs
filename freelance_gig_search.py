#!/usr/bin/env python
"""
Freelance Gig Search Module for MERN Stack Developers
----------------------------------------------------
This module provides specialized search capabilities for freelance web development gigs,
particularly focused on MERN stack opportunities across multiple freelance platforms.
"""

import requests
import pandas as pd
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import streamlit as st

@dataclass
class FreelanceGig:
    """Data structure for freelance gig information"""
    title: str
    description: str
    budget_min: Optional[float]
    budget_max: Optional[float]
    currency: str
    skills_required: List[str]
    client_rating: Optional[float]
    client_reviews: Optional[int]
    posted_date: str
    project_type: str  # hourly, fixed, recurring
    experience_level: str  # entry, intermediate, expert
    duration: Optional[str]
    url: str
    platform: str
    is_remote: bool = True

class FreelancePlatformSearcher:
    """Base class for freelance platform scrapers"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_gigs(self, query: str, max_results: int = 50) -> List[FreelanceGig]:
        """Search for gigs on the platform"""
        raise NotImplementedError
    
    def _parse_budget(self, budget_str: str) -> Tuple[Optional[float], Optional[float]]:
        """Parse budget string to min/max values"""
        if not budget_str:
            return None, None
        
        # Remove currency symbols and common words
        budget_str = budget_str.replace('$', '').replace('USD', '').replace('€', '').replace('£', '')
        budget_str = budget_str.replace('Fixed Price', '').replace('Hourly', '').strip()
        
        try:
            if '-' in budget_str:
                parts = budget_str.split('-')
                min_val = float(parts[0].strip().replace(',', ''))
                max_val = float(parts[1].strip().replace(',', ''))
                return min_val, max_val
            else:
                val = float(budget_str.replace(',', ''))
                return val, val
        except:
            return None, None

class UpworkSearcher(FreelancePlatformSearcher):
    """Upwork gig searcher using their public API"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.base_url = "https://www.upwork.com"
    
    def search_gigs(self, query: str, max_results: int = 50) -> List[FreelanceGig]:
        """Search Upwork for gigs (simulated - requires API access)"""
        # Note: Upwork requires API access. This is a demonstration structure
        gigs = []
        
        # MERN stack specific search terms
        mern_terms = [
            "MERN stack developer",
            "React Node.js MongoDB",
            "full stack JavaScript",
            "MongoDB Express React Node",
            "React developer with Node.js",
            "full stack web development",
            "JavaScript full stack",
            "React frontend with Node backend"
        ]
        
        # For demonstration, we'll create sample gigs
        # In production, you'd use Upwork's API
        sample_gigs = [
            {
                "title": "MERN Stack Developer for E-commerce Platform",
                "description": "Need a skilled MERN stack developer to build a modern e-commerce platform with React frontend, Node.js backend, and MongoDB database.",
                "budget": "$2000-$5000",
                "skills": ["React", "Node.js", "MongoDB", "Express", "JavaScript"],
                "client_rating": 4.8,
                "client_reviews": 45,
                "project_type": "Fixed Price",
                "experience_level": "Intermediate",
                "duration": "2-3 months"
            },
            {
                "title": "React Developer with Node.js Backend Experience",
                "description": "Looking for a React developer who can also handle Node.js backend development. Project involves building a real-time chat application.",
                "budget": "$1500-$3000",
                "skills": ["React", "Node.js", "Socket.io", "MongoDB"],
                "client_rating": 4.6,
                "client_reviews": 23,
                "project_type": "Fixed Price",
                "experience_level": "Entry",
                "duration": "1-2 months"
            }
        ]
        
        for gig_data in sample_gigs:
            min_budget, max_budget = self._parse_budget(gig_data["budget"])
            gig = FreelanceGig(
                title=gig_data["title"],
                description=gig_data["description"],
                budget_min=min_budget,
                budget_max=max_budget,
                currency="USD",
                skills_required=gig_data["skills"],
                client_rating=gig_data["client_rating"],
                client_reviews=gig_data["client_reviews"],
                posted_date=datetime.now().strftime("%Y-%m-%d"),
                project_type=gig_data["project_type"],
                experience_level=gig_data["experience_level"],
                duration=gig_data["duration"],
                url=f"{self.base_url}/jobs/~{hash(gig_data['title'])}",
                platform="Upwork"
            )
            gigs.append(gig)
        
        return gigs[:max_results]

class FiverrSearcher(FreelancePlatformSearcher):
    """Fiverr gig searcher"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.fiverr.com"
    
    def search_gigs(self, query: str, max_results: int = 50) -> List[FreelanceGig]:
        """Search Fiverr for gigs"""
        gigs = []
        
        # Fiverr search simulation
        sample_gigs = [
            {
                "title": "Build Complete MERN Stack Web Application",
                "description": "I will develop a complete MERN stack web application with React frontend, Node.js backend, and MongoDB database. Includes authentication, API development, and deployment.",
                "budget": "$500-$2000",
                "skills": ["React", "Node.js", "MongoDB", "Express", "JavaScript", "REST API"],
                "client_rating": 5.0,
                "client_reviews": 127,
                "project_type": "Fixed Price",
                "experience_level": "Expert",
                "duration": "5-10 days"
            },
            {
                "title": "React Frontend Development with Node.js Backend",
                "description": "Professional React frontend development with Node.js backend integration. Clean code, responsive design, and modern UI/UX.",
                "budget": "$200-$800",
                "skills": ["React", "Node.js", "JavaScript", "CSS", "HTML"],
                "client_rating": 4.9,
                "client_reviews": 89,
                "project_type": "Fixed Price",
                "experience_level": "Intermediate",
                "duration": "3-7 days"
            }
        ]
        
        for gig_data in sample_gigs:
            min_budget, max_budget = self._parse_budget(gig_data["budget"])
            gig = FreelanceGig(
                title=gig_data["title"],
                description=gig_data["description"],
                budget_min=min_budget,
                budget_max=max_budget,
                currency="USD",
                skills_required=gig_data["skills"],
                client_rating=gig_data["client_rating"],
                client_reviews=gig_data["client_reviews"],
                posted_date=datetime.now().strftime("%Y-%m-%d"),
                project_type=gig_data["project_type"],
                experience_level=gig_data["experience_level"],
                duration=gig_data["duration"],
                url=f"{self.base_url}/services/{hash(gig_data['title'])}",
                platform="Fiverr"
            )
            gigs.append(gig)
        
        return gigs[:max_results]

class FreelancerSearcher(FreelancePlatformSearcher):
    """Freelancer.com gig searcher"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.freelancer.com"
    
    def search_gigs(self, query: str, max_results: int = 50) -> List[FreelanceGig]:
        """Search Freelancer.com for gigs"""
        gigs = []
        
        # Freelancer.com search simulation
        sample_gigs = [
            {
                "title": "MERN Stack Developer Needed for Startup",
                "description": "Startup looking for experienced MERN stack developer to build MVP. Must have experience with React, Node.js, MongoDB, and deployment.",
                "budget": "$3000-$8000",
                "skills": ["React", "Node.js", "MongoDB", "Express", "AWS", "Docker"],
                "client_rating": 4.7,
                "client_reviews": 34,
                "project_type": "Fixed Price",
                "experience_level": "Expert",
                "duration": "3-6 months"
            },
            {
                "title": "React Developer for E-commerce Website",
                "description": "Need a React developer to build an e-commerce website with Node.js backend. Should include payment integration and admin panel.",
                "budget": "$1000-$2500",
                "skills": ["React", "Node.js", "Stripe", "MongoDB", "E-commerce"],
                "client_rating": 4.5,
                "client_reviews": 18,
                "project_type": "Fixed Price",
                "experience_level": "Intermediate",
                "duration": "1-2 months"
            }
        ]
        
        for gig_data in sample_gigs:
            min_budget, max_budget = self._parse_budget(gig_data["budget"])
            gig = FreelanceGig(
                title=gig_data["title"],
                description=gig_data["description"],
                budget_min=min_budget,
                budget_max=max_budget,
                currency="USD",
                skills_required=gig_data["skills"],
                client_rating=gig_data["client_rating"],
                client_reviews=gig_data["client_reviews"],
                posted_date=datetime.now().strftime("%Y-%m-%d"),
                project_type=gig_data["project_type"],
                experience_level=gig_data["experience_level"],
                duration=gig_data["duration"],
                url=f"{self.base_url}/projects/{hash(gig_data['title'])}",
                platform="Freelancer.com"
            )
            gigs.append(gig)
        
        return gigs[:max_results]

class UnifiedFreelanceSearcher:
    """Unified searcher for multiple freelance platforms"""
    
    def __init__(self):
        self.searchers = {
            "upwork": UpworkSearcher(),
            "fiverr": FiverrSearcher(),
            "freelancer": FreelancerSearcher()
        }
    
    def search_all_platforms(self, 
                           query: str, 
                           platforms: List[str] = None,
                           max_results_per_platform: int = 20,
                           min_budget: Optional[float] = None,
                           max_budget: Optional[float] = None,
                           experience_level: Optional[str] = None,
                           project_type: Optional[str] = None) -> pd.DataFrame:
        """
        Search across multiple freelance platforms
        
        Args:
            query: Search query
            platforms: List of platforms to search (upwork, fiverr, freelancer)
            max_results_per_platform: Maximum results per platform
            min_budget: Minimum budget filter
            max_budget: Maximum budget filter
            experience_level: Experience level filter (entry, intermediate, expert)
            project_type: Project type filter (Fixed Price, Hourly, etc.)
        
        Returns:
            DataFrame with all gigs
        """
        if platforms is None:
            platforms = ["upwork", "fiverr", "freelancer"]
        
        all_gigs = []
        
        for platform in platforms:
            if platform in self.searchers:
                try:
                    gigs = self.searchers[platform].search_gigs(query, max_results_per_platform)
                    all_gigs.extend(gigs)
                except Exception as e:
                    st.warning(f"Error searching {platform}: {str(e)}")
        
        # Convert to DataFrame
        if all_gigs:
            df_data = []
            for gig in all_gigs:
                df_data.append({
                    'title': gig.title,
                    'description': gig.description,
                    'budget_min': gig.budget_min,
                    'budget_max': gig.budget_max,
                    'currency': gig.currency,
                    'skills_required': ', '.join(gig.skills_required),
                    'client_rating': gig.client_rating,
                    'client_reviews': gig.client_reviews,
                    'posted_date': gig.posted_date,
                    'project_type': gig.project_type,
                    'experience_level': gig.experience_level,
                    'duration': gig.duration,
                    'url': gig.url,
                    'platform': gig.platform,
                    'is_remote': gig.is_remote
                })
            
            df = pd.DataFrame(df_data)
            
            # Apply filters
            if min_budget is not None:
                df = df[df['budget_min'] >= min_budget]
            
            if max_budget is not None:
                df = df[df['budget_max'] <= max_budget]
            
            if experience_level:
                df = df[df['experience_level'].str.contains(experience_level, case=False, na=False)]
            
            if project_type:
                df = df[df['project_type'].str.contains(project_type, case=False, na=False)]
            
            return df
        else:
            return pd.DataFrame()

def get_mern_stack_search_queries() -> Dict[str, str]:
    """Get optimized search queries for MERN stack developers"""
    return {
        "MERN Stack Development": "MERN stack OR React Node.js MongoDB OR full stack JavaScript",
        "React Frontend": "React developer OR React.js OR React frontend",
        "Node.js Backend": "Node.js developer OR Express.js OR Node.js backend",
        "MongoDB Database": "MongoDB developer OR MongoDB database OR NoSQL",
        "Full Stack JavaScript": "full stack JavaScript OR JavaScript full stack OR MEAN stack",
        "Web Development": "web developer OR web development OR JavaScript developer",
        "API Development": "API developer OR REST API OR API development",
        "E-commerce Development": "e-commerce developer OR online store OR shopping cart",
        "Real-time Applications": "real-time OR Socket.io OR WebSocket OR chat application",
        "Progressive Web Apps": "PWA OR progressive web app OR mobile web app"
    }

def search_mern_freelance_gigs(query_category: str = "MERN Stack Development",
                              platforms: List[str] = None,
                              max_results_per_platform: int = 20,
                              min_budget: float = 0,
                              max_budget: float = 10000,
                              experience_level: str = None) -> pd.DataFrame:
    """
    Search for MERN stack freelance gigs
    
    Args:
        query_category: Category from get_mern_stack_search_queries()
        platforms: List of platforms to search
        max_results_per_platform: Max results per platform
        min_budget: Minimum budget filter
        max_budget: Maximum budget filter
        experience_level: Experience level filter
    
    Returns:
        DataFrame with MERN stack gigs
    """
    queries = get_mern_stack_search_queries()
    
    if query_category not in queries:
        raise ValueError(f"Invalid category. Available: {list(queries.keys())}")
    
    searcher = UnifiedFreelanceSearcher()
    
    return searcher.search_all_platforms(
        query=queries[query_category],
        platforms=platforms,
        max_results_per_platform=max_results_per_platform,
        min_budget=min_budget,
        max_budget=max_budget,
        experience_level=experience_level
    )

# Example usage
if __name__ == "__main__":
    # Search for MERN stack gigs
    gigs_df = search_mern_freelance_gigs(
        query_category="MERN Stack Development",
        platforms=["upwork", "fiverr", "freelancer"],
        max_results_per_platform=10,
        min_budget=500,
        max_budget=5000
    )
    
    print(f"Found {len(gigs_df)} MERN stack gigs")
    if not gigs_df.empty:
        print(gigs_df[['title', 'platform', 'budget_min', 'budget_max', 'experience_level']].head())
        
        # Save to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mern_freelance_gigs_{timestamp}.csv"
        gigs_df.to_csv(filename, index=False)
        print(f"Results saved to {filename}") 