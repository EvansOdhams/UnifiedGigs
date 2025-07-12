#!/usr/bin/env python
"""
MERN Stack Freelance Gig Search Example
---------------------------------------
This example demonstrates how to use the enhanced UnifiedGigs application
to search for freelance opportunities specifically for MERN stack developers.
"""

import pandas as pd
from freelance_gig_search import search_mern_freelance_gigs, get_mern_stack_search_queries
import datetime
import csv

def main():
    """Main function to demonstrate MERN stack freelance gig search"""
    
    print("🚀 MERN Stack Freelance Gig Search Example")
    print("=" * 50)
    
    # Show available search categories
    print("\n📋 Available MERN Stack Search Categories:")
    categories = get_mern_stack_search_queries()
    for i, (category, query) in enumerate(categories.items(), 1):
        print(f"{i}. {category}")
    
    # Search for MERN stack development gigs
    print("\n🔍 Searching for MERN Stack Development gigs...")
    
    try:
        # Search across all platforms
        gigs_df = search_mern_freelance_gigs(
            query_category="MERN Stack Development",
            platforms=["upwork", "fiverr", "freelancer"],
            max_results_per_platform=5,
            min_budget=500,
            max_budget=5000,
            experience_level="intermediate"
        )
        
        if not gigs_df.empty:
            print(f"\n✅ Found {len(gigs_df)} MERN stack gigs!")
            
            # Display summary
            print("\n📊 Gig Summary:")
            print(f"Total Gigs: {len(gigs_df)}")
            print(f"Average Budget: ${gigs_df['budget_min'].mean():.0f} - ${gigs_df['budget_max'].mean():.0f}")
            print(f"Platforms: {', '.join(gigs_df['platform'].unique())}")
            
            # Show top gigs
            print("\n🔥 Top MERN Stack Gigs:")
            for i, gig in gigs_df.head(3).iterrows():
                print(f"\n{i+1}. {gig['title']}")
                print(f"   Platform: {gig['platform']}")
                print(f"   Budget: ${gig['budget_min']} - ${gig['budget_max']} {gig['currency']}")
                print(f"   Experience: {gig['experience_level']}")
                print(f"   Duration: {gig['duration']}")
                print(f"   Client Rating: {gig['client_rating']} ({gig['client_reviews']} reviews)")
                print(f"   Skills: {gig['skills_required']}")
            
            # Save results
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mern_freelance_gigs_{timestamp}.csv"
            gigs_df.to_csv(filename, index=False)
            print(f"\n💾 Results saved to: {filename}")
            
            # Show budget analysis
            print("\n💰 Budget Analysis:")
            budget_ranges = [
                (0, 1000, "Low Budget"),
                (1000, 3000, "Medium Budget"),
                (3000, 10000, "High Budget")
            ]
            
            for min_b, max_b, label in budget_ranges:
                count = len(gigs_df[
                    (gigs_df['budget_min'] >= min_b) & 
                    (gigs_df['budget_max'] <= max_b)
                ])
                print(f"   {label} (${min_b}-${max_b}): {count} gigs")
            
        else:
            print("❌ No gigs found matching your criteria.")
            print("💡 Try adjusting your search parameters:")
            print("   - Lower the minimum budget")
            print("   - Remove experience level filter")
            print("   - Try different categories")
    
    except Exception as e:
        print(f"❌ Error during search: {str(e)}")
        print("💡 This is a demonstration with sample data.")
        print("   In production, you would need API access to real platforms.")

def search_by_category(category_name: str):
    """Search for gigs in a specific category"""
    print(f"\n🔍 Searching for {category_name} gigs...")
    
    try:
        gigs_df = search_mern_freelance_gigs(
            query_category=category_name,
            platforms=["upwork", "fiverr", "freelancer"],
            max_results_per_platform=3
        )
        
        if not gigs_df.empty:
            print(f"✅ Found {len(gigs_df)} {category_name} gigs!")
            print("\nTop gigs:")
            for i, gig in gigs_df.head(2).iterrows():
                print(f"  • {gig['title']} (${gig['budget_min']}-${gig['budget_max']})")
        else:
            print(f"❌ No {category_name} gigs found.")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def demonstrate_categories():
    """Demonstrate searching different categories"""
    print("\n🎯 Demonstrating Different Categories:")
    
    categories_to_demo = [
        "React Frontend",
        "Node.js Backend", 
        "API Development",
        "E-commerce Development"
    ]
    
    for category in categories_to_demo:
        search_by_category(category)

if __name__ == "__main__":
    # Run main search
    main()
    
    # Demonstrate different categories
    demonstrate_categories()
    
    print("\n" + "=" * 50)
    print("🎉 Example completed!")
    print("\n💡 Next Steps:")
    print("1. Run 'streamlit run app_enhanced.py' to use the web interface")
    print("2. Customize search parameters for your needs")
    print("3. Set up API keys for real platform access")
    print("4. Integrate with your existing job search workflow") 