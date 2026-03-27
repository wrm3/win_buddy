---
name: business-operations
description: Comprehensive guide for HR, compensation, benefits, and accounting/finance operations. Covers hiring, payroll, equity, benefits administration, bookkeeping, and financial management. Use when working with HR, compensation, or finance tasks.
triggers:
  - "hire"
  - "employee"
  - "salary"
  - "compensation"
  - "benefits"
  - "401k"
  - "equity"
  - "stock options"
  - "accounting"
  - "bookkeeping"
  - "taxes"
  - "payroll"
  - "financial statements"
agents:
  - hr-specialist
  - compensation-benefits-specialist
  - accounting-finance-specialist
version: 1.0.0
---

# Business Operations Skill

Comprehensive reference for HR, compensation & benefits, and accounting/finance operations. This skill supports three specialized agents:

- **hr-specialist**: Hiring, onboarding, employee relations, policies
- **compensation-benefits-specialist**: Salary, equity, benefits packages
- **accounting-finance-specialist**: Bookkeeping, financial statements, taxes

## ⚠️ Important Disclaimer

**This skill provides educational information only, not legal, tax, or financial advice.**
- Consult employment attorneys for HR legal matters
- Consult CPAs for tax and accounting matters
- Consult benefits brokers for benefits design
- Laws vary by state and change frequently

---

## HR Operations

### Hiring Process Timeline

| Stage | Duration | Activities |
|-------|----------|------------|
| Job Posting | 1-2 weeks | Write JD, post to boards |
| Sourcing | 2-4 weeks | Review applications, source |
| Screening | 1-2 weeks | Phone screens, assessments |
| Interviews | 2-3 weeks | Technical, behavioral, final |
| Offer | 1 week | Extend, negotiate, close |
| **Total** | **7-12 weeks** | |

### Job Description Template

```markdown
# [Job Title]

## About Us
[2-3 sentences about company]

## The Role
[What they'll do, impact they'll have]

## Responsibilities
- [Key responsibility 1]
- [Key responsibility 2]
- [Key responsibility 3]

## Requirements
- [Must-have 1]
- [Must-have 2]
- [Must-have 3]

## Nice to Have
- [Preferred qualification 1]
- [Preferred qualification 2]

## What We Offer
- Competitive salary: $[range]
- Equity: [X]%
- Benefits: [Health, 401k, etc.]
- [Other perks]

## How to Apply
[Instructions]
```

### Interview Scorecard

```markdown
Candidate: _______________
Position: _______________
Interviewer: _______________
Date: _______________

## Technical Skills (1-4)
| Skill | Score | Notes |
|-------|-------|-------|
| [Skill 1] | | |
| [Skill 2] | | |
| [Skill 3] | | |

## Behavioral (1-4)
| Competency | Score | Notes |
|------------|-------|-------|
| Communication | | |
| Problem Solving | | |
| Collaboration | | |
| Culture Fit | | |

## Overall
- Score: ___ / 4
- Recommendation: [ ] Strong Hire [ ] Hire [ ] No Hire [ ] Strong No Hire
- Comments:
```

### Employee Classification

| Type | Characteristics | Tax Forms |
|------|-----------------|-----------|
| **W-2 Employee** | Set hours, company equipment, ongoing | W-4, I-9, W-2 |
| **1099 Contractor** | Own schedule, own tools, project-based | W-9, 1099-NEC |

**Misclassification Risk**: IRS looks at:
- Behavioral control (how work is done)
- Financial control (payment method, expenses)
- Relationship type (benefits, permanence)

### Onboarding Checklist

```
□ Pre-Start
  □ Send offer letter
  □ Collect signed documents
  □ Order equipment
  □ Set up accounts (email, Slack, etc.)
  □ Assign buddy/mentor

□ Day 1
  □ Welcome and introductions
  □ HR paperwork (I-9, W-4, benefits enrollment)
  □ Equipment setup
  □ Security/access setup
  □ Company overview presentation

□ Week 1
  □ Team introductions
  □ Role-specific training
  □ 1:1 with manager
  □ Review goals and expectations
  □ Buddy check-in

□ Day 30
  □ Manager check-in
  □ Feedback collection
  □ Adjust onboarding as needed

□ Day 90
  □ Performance check-in
  □ Goal review
  □ End of probation (if applicable)
```

---

## Compensation & Benefits

### Salary Benchmarking Sources

| Source | Type | Cost | Best For |
|--------|------|------|----------|
| Levels.fyi | Self-reported | Free | Tech roles |
| Glassdoor | Self-reported | Free | General |
| Pave | Verified | $$ | Startups |
| Radford | Survey | $$$ | Enterprise |
| Mercer | Survey | $$$ | Enterprise |

### Pay Band Structure

```
Level: Senior Engineer (IC4)

        Min         Mid         Max
        |-----------|-----------|
        $160,000    $180,000    $200,000
        
Placement factors:
- Experience within level
- Specific skills/expertise
- Internal equity
- Market conditions
```

### Equity Compensation Guide

| Stage | Role | Equity Range |
|-------|------|--------------|
| **Seed** | First engineer | 1.0-2.0% |
| | Engineer #2-5 | 0.5-1.0% |
| | First non-tech | 0.5-1.0% |
| **Series A** | Senior IC | 0.15-0.30% |
| | Manager | 0.25-0.50% |
| | Director | 0.50-1.0% |
| **Series B+** | Senior IC | 0.05-0.15% |
| | Manager | 0.10-0.25% |
| | Director | 0.25-0.50% |

### Stock Option Types

| Type | Tax at Grant | Tax at Exercise | Tax at Sale |
|------|--------------|-----------------|-------------|
| **ISO** | None | AMT may apply | LTCG if held 2yr/1yr |
| **NSO** | None | Ordinary income | STCG or LTCG |
| **RSU** | None | Ordinary income | STCG or LTCG |

**83(b) Election**: File within 30 days of restricted stock grant to be taxed at grant value (not vesting value).

### Benefits Package by Stage

**Seed (1-10 employees)**
```
Essential:
- Health insurance (via PEO)
- Unlimited PTO
- Remote work flexibility

Cost: ~$500-800/employee/month
```

**Series A (10-30 employees)**
```
Add:
- Dental & Vision
- 401(k) (no match initially)
- Life insurance
- Parental leave (8-12 weeks)

Cost: ~$800-1,200/employee/month
```

**Series B+ (30+ employees)**
```
Add:
- 401(k) match (3-4%)
- Extended parental leave (16+ weeks)
- Professional development budget
- Wellness stipend
- Commuter benefits

Cost: ~$1,200-1,800/employee/month
```

### 401(k) Options

| Type | Match | Vesting | Testing |
|------|-------|---------|---------|
| Traditional | Discretionary | Up to 6 years | Required |
| Safe Harbor | 3-4% required | Immediate | Exempt |
| SIMPLE | 3% or 2% | Immediate | Exempt |

**Safe Harbor** recommended for startups (avoids testing, immediate vesting).

---

## Accounting & Finance

### Chart of Accounts (Startup)

```
ASSETS (1000s)
1000 Cash
1100 Accounts Receivable
1200 Prepaid Expenses
1500 Fixed Assets

LIABILITIES (2000s)
2000 Accounts Payable
2100 Credit Cards
2200 Accrued Expenses
2300 Deferred Revenue
2400 Notes Payable

EQUITY (3000s)
3000 Common Stock
3100 Preferred Stock
3200 APIC
3300 Retained Earnings

REVENUE (4000s)
4000 Product Revenue
4100 Service Revenue

COGS (5000s)
5000 Hosting
5100 Payment Processing

EXPENSES (6000s)
6000 Payroll
6100 Sales & Marketing
6200 G&A
6300 R&D
```

### Monthly Close Checklist

```
□ Week 1: Transactions
  □ Categorize all transactions
  □ Review credit card statements
  □ Process expense reports
  □ Record payroll entries

□ Week 2: Reconciliation
  □ Bank reconciliation
  □ Credit card reconciliation
  □ AR aging review
  □ AP aging review

□ Week 3: Accruals & Adjustments
  □ Record accrued expenses
  □ Recognize deferred revenue
  □ Record depreciation
  □ Prepaid expense amortization

□ Week 4: Review & Report
  □ Review P&L
  □ Review Balance Sheet
  □ Prepare board package
  □ Document any issues
```

### Financial Statements

**Income Statement (P&L)**
```
Revenue
- Cost of Revenue
= Gross Profit
- Operating Expenses
  - Sales & Marketing
  - General & Administrative
  - Research & Development
= Operating Income (EBITDA)
- Interest & Taxes
= Net Income
```

**Key Metrics**
| Metric | Formula | Target |
|--------|---------|--------|
| Gross Margin | (Revenue - COGS) / Revenue | >70% SaaS |
| Burn Rate | Monthly cash decrease | Depends |
| Runway | Cash / Burn Rate | >12 months |
| CAC | Sales+Marketing / New Customers | <LTV/3 |
| LTV | ARPU × Gross Margin / Churn | >3× CAC |

### Tax Calendar (US)

| Date | Filing | Who |
|------|--------|-----|
| Jan 31 | W-2s to employees | All employers |
| Jan 31 | 1099s to contractors | If paid >$600 |
| Mar 1 | Delaware Franchise Tax | DE corps |
| Mar 15 | S-Corp/Partnership returns | S-Corps, LLCs |
| Apr 15 | C-Corp returns (or extension) | C-Corps |
| Apr 15 | Q1 estimated taxes | All |
| Jun 15 | Q2 estimated taxes | All |
| Sep 15 | Q3 estimated taxes | All |
| Jan 15 | Q4 estimated taxes | All |

### Runway Calculator

```
Runway (months) = Cash / Monthly Burn Rate

Example:
Cash: $500,000
Monthly Burn: $40,000
Runway: 12.5 months

When to fundraise: 12-18 months before you need money
When to cut costs: <6 months runway
```

### Accounting Software Comparison

| Software | Best For | Cost |
|----------|----------|------|
| QuickBooks Online | Most startups | $30-200/mo |
| Xero | International | $13-70/mo |
| Wave | Very early stage | Free |
| NetSuite | Growth stage | $$$$ |

---

## Compliance Checklist

### Federal (All US Companies)

```
□ EIN obtained
□ I-9 for all employees
□ W-4 for all employees
□ Quarterly 941 payroll tax filings
□ Annual W-2s and 1099s
□ OSHA compliance (if applicable)
□ FLSA compliance (overtime, minimum wage)
```

### State (Varies)

```
□ State tax registration
□ Unemployment insurance
□ Workers' compensation
□ State-specific leave laws
□ Pay transparency requirements
□ Harassment training (CA, NY, etc.)
```

### Delaware Corporation

```
□ Annual Franchise Tax (March 1)
□ Annual Report
□ Registered agent maintained
□ Stock ledger maintained
□ Board meeting minutes
```

---

## Templates & Resources

### Reference Documents
- `reference/employment_law.md` - Key employment laws
- `reference/benefits_comparison.md` - Benefits options
- `reference/tax_calendar.md` - Tax deadlines
- `reference/compliance_by_state.md` - State requirements

### Templates
- `templates/offer_letter.md` - Offer letter template
- `templates/employee_handbook.md` - Handbook template
- `templates/job_description.md` - JD template
- `templates/performance_review.md` - Review template
- `templates/pip.md` - PIP template

### External Resources
- [IRS Employer Tax Guide](https://www.irs.gov/businesses/small-businesses-self-employed/employer-id-numbers)
- [DOL Wage & Hour](https://www.dol.gov/agencies/whd)
- [SHRM](https://www.shrm.org) - HR resources
- [Gusto](https://gusto.com) - Payroll/HR platform

---
*This skill supports: hr-specialist, compensation-benefits-specialist, accounting-finance-specialist agents*
