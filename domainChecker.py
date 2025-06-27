#!/usr/bin/env python3
"""
Domain Availability Checker

This script checks the availability of domain names using whois lookup.
It can accept a single domain or multiple domains as command line arguments.

Usage:
    python domain_checker.py example.com
    python domain_checker.py example.com google.com test123.com
"""

import sys
import argparse
import whois
from typing import List, Tuple
from tqdm import tqdm


def get_minimum_cost(domain: str, is_available: bool) -> str:
    """Get the minimum cost for a domain if it's available."""
    if not is_available:
        return ""
    
    if domain.endswith('.ai'):
        return "$200"
    elif domain.endswith('.com'):
        return "$10"
    elif domain.endswith('.io'):
        return "$50"
    else:
        return ""


def check_domain_availability(domain: str) -> Tuple[str, bool, str, str]:
    """
    Check if a domain is available for registration.
    
    Args:
        domain (str): Domain name to check
        
    Returns:
        Tuple[str, bool, str, str]: (domain, is_available, minimum_cost, year_registered)
    """
    try:
        # Clean the domain (remove http/https and www if present)
        domain = domain.lower().strip()
        if domain.startswith(('http://', 'https://')):
            domain = domain.split('//', 1)[1]
        if domain.startswith('www.'):
            domain = domain[4:]
        
        # Perform whois lookup
        domain_info = whois.whois(domain)
        
        # Check various indicators that suggest domain is registered
        if domain_info is None:
            is_available = True
            cost = get_minimum_cost(domain, is_available)
            return domain, is_available, cost, ""
        
        # Extract creation date/year if available
        creation_year = ""
        if hasattr(domain_info, 'creation_date') and domain_info.creation_date:
            creation_date = domain_info.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0] if creation_date else None
            if creation_date:
                try:
                    creation_year = str(creation_date.year)
                except (AttributeError, TypeError):
                    # Handle case where creation_date might be a string
                    creation_year = str(creation_date)[:4] if len(str(creation_date)) >= 4 else ""
        
        # Check if domain has registration data
        if hasattr(domain_info, 'status') and domain_info.status:
            if isinstance(domain_info.status, list):
                status_list = [str(s).lower() for s in domain_info.status]
            else:
                status_list = [str(domain_info.status).lower()]
            
            # If any status indicates the domain is registered/active
            active_statuses = ['ok', 'active', 'clienttransferprohibited', 'clientdeleteprohibited']
            if any(status in ' '.join(status_list) for status in active_statuses):
                is_available = False
                cost = get_minimum_cost(domain, is_available)
                return domain, is_available, cost, creation_year
        
        # Check if domain has registrar information
        if hasattr(domain_info, 'registrar') and domain_info.registrar:
            is_available = False
            cost = get_minimum_cost(domain, is_available)
            return domain, is_available, cost, creation_year
        
        # Check if domain has creation date
        if hasattr(domain_info, 'creation_date') and domain_info.creation_date:
            is_available = False
            cost = get_minimum_cost(domain, is_available)
            return domain, is_available, cost, creation_year
        
        # Check if domain has expiration date
        if hasattr(domain_info, 'expiration_date') and domain_info.expiration_date:
            is_available = False
            cost = get_minimum_cost(domain, is_available)
            return domain, is_available, cost, creation_year
        
        # If we get whois data but no clear registration indicators, it might be available
        is_available = True
        cost = get_minimum_cost(domain, is_available)
        return domain, is_available, cost, ""
        
    except whois.parser.PywhoisError as e:
        error_msg = str(e).lower()
        if 'no match' in error_msg or 'not found' in error_msg or 'no entries found' in error_msg:
            is_available = True
            cost = get_minimum_cost(domain, is_available)
            return domain, is_available, cost, ""
        else:
            is_available = False
            cost = get_minimum_cost(domain, is_available)
            return domain, is_available, cost, ""
    
    except Exception as e:
        is_available = False
        cost = get_minimum_cost(domain, is_available)
        return domain, is_available, cost, ""


def format_result(domain: str, is_available: bool, minimum_cost: str, year_registered: str) -> str:
    """Format the result for display."""
    status = "✅ AVAILABLE" if is_available else "❌ TAKEN"
    cost_display = minimum_cost if minimum_cost else ""
    # year_display = year_registered if year_registered else ""  # Commented out since we only show available
    return f"{domain:<40} | {status:<12} | {cost_display:<12}"


def main():
    parser = argparse.ArgumentParser(
        description='Check domain availability using whois lookup',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python domain_checker.py example.com
  python domain_checker.py example.com google.com test123.com
        """
    )
    
    parser.add_argument(
        'domains',
        nargs='+',
        help='One or more domain names to check'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show verbose output'
    )
    
    args = parser.parse_args()
    
    print("Domain Availability Checker")
    print("=" * 80)
    print(f"{'Domain':<40} | {'Status':<12} | {'Minimum Cost':<12}")
    print("-" * 80)
    
    available_domains = []
    taken_domains = []
    all_results = []
    
    # Expand .com domains to include .ai and .io versions
    domains_to_check = []
    for domain in args.domains:
        domains_to_check.append(domain)
        if domain.endswith('.com'):
            base_name = domain[:-4]  # Remove .com extension
            domains_to_check.append(f"{base_name}.ai")
            domains_to_check.append(f"{base_name}.io")
    
    # Collect all results first with progress bar
    print(f"Checking {len(domains_to_check)} domains...")
    
    progress_bar = tqdm(domains_to_check, desc="Progress", unit="domain")
    for domain in progress_bar:
        # Update progress bar to show current domain
        progress_bar.set_postfix_str(f"{domain}")
        
        domain, is_available, minimum_cost, year_registered = check_domain_availability(domain)
        all_results.append((domain, is_available, minimum_cost, year_registered))
        
        if is_available:
            available_domains.append(domain)
        else:
            taken_domains.append(domain)
    
    # Close progress bar and clear all progress lines
    progress_bar.close()
    print("\033[A\033[K", end="")  # Move up one line and clear progress bar
    print("\033[A\033[K", end="")  # Move up one line and clear "Checking X domains..."
    
    # Sort results: available domains first, then by price (cheapest first), then alphabetically
    def sort_key(result):
        domain, is_available, minimum_cost, year_registered = result
        # Extract numeric price from cost string (e.g., "$10" -> 10)
        if is_available and minimum_cost:
            try:
                price = int(minimum_cost.replace('$', ''))
            except ValueError:
                price = 999  # fallback for parsing errors
        else:
            price = 999  # taken domains get high price for sorting
        
        # Return tuple: (availability_priority, price, domain_name)
        # availability_priority: 0 for available, 1 for taken (so available comes first)
        availability_priority = 0 if is_available else 1
        return (availability_priority, price, domain.lower())
    
    all_results.sort(key=sort_key)
    
    # Print only available domains (filtered results)
    available_results = [(domain, is_available, minimum_cost, year_registered) 
                        for domain, is_available, minimum_cost, year_registered in all_results 
                        if is_available]
    
    for domain, is_available, minimum_cost, year_registered in available_results:
        print(format_result(domain, is_available, minimum_cost, year_registered))
    
    print("-" * 80)
    print(f"Summary: {len(args.domains)} domains provided, {len(domains_to_check)} checked, {len(available_domains)} available")
    
    if args.verbose:
        if available_domains:
            print(f"\nAvailable domains: {', '.join(available_domains)}")
        if taken_domains:
            print(f"Taken domains: {', '.join(taken_domains)}")


if __name__ == "__main__":
    main() 