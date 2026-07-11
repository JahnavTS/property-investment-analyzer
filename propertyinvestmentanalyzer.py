

from dataclasses import dataclass


@dataclass
class Property:
    name: str
    area: str
    price: float          # purchase price (AED)
    monthly_rent: float    # expected monthly rent (AED)
    size_sqft: float       # size in square feet


def rental_yield(prop: Property) -> float:
    """Gross annual rental yield as a percentage of purchase price."""
    annual_rent = prop.monthly_rent * 12
    return (annual_rent / prop.price) * 100


def price_per_sqft(prop: Property) -> float:
    return prop.price / prop.size_sqft


def estimated_roi(prop: Property, years: int, annual_appreciation_pct: float = 0.0) -> float:
    """
    Simple ROI over N years:
    total return = (rent collected over N years + appreciation) / price
    """
    annual_rent = prop.monthly_rent * 12
    total_rent = annual_rent * years
    appreciation_value = prop.price * ((1 + annual_appreciation_pct / 100) ** years - 1)
    total_return = total_rent + appreciation_value
    roi_pct = (total_return / prop.price) * 100
    return roi_pct


def rank_properties(properties: list[Property], years: int = 5, appreciation_pct: float = 3.0):
    """Rank properties by a simple composite investment score (higher = better)."""
    results = []
    for p in properties:
        yield_pct = rental_yield(p)
        ppsf = price_per_sqft(p)
        roi = estimated_roi(p, years, appreciation_pct)
        # Simple composite score: weight yield and ROI, penalize high price/sqft slightly
        score = (yield_pct * 0.4) + (roi / years * 0.5) - (ppsf / 1000 * 0.1)
        results.append({
            "name": p.name,
            "area": p.area,
            "price": p.price,
            "yield_pct": round(yield_pct, 2),
            "price_per_sqft": round(ppsf, 2),
            "roi_over_years": round(roi, 2),
            "score": round(score, 2),
        })
    results.sort(key=lambda r: r["score"], reverse=True)
    return results


def print_report(results: list[dict], years: int):
    print(f"\n{'PROPERTY INVESTMENT ANALYSIS':^80}")
    print(f"{'(Ranked by ' + str(years) + '-year investment score)':^80}\n")
    header = f"{'Rank':<5}{'Property':<20}{'Area':<15}{'Yield %':<10}{'AED/sqft':<12}{'ROI %':<10}{'Score':<8}"
    print(header)
    print("-" * len(header))
    for i, r in enumerate(results, start=1):
        print(f"{i:<5}{r['name']:<20}{r['area']:<15}{r['yield_pct']:<10}{r['price_per_sqft']:<12}"
              f"{r['roi_over_years']:<10}{r['score']:<8}")
    print()


if __name__ == "__main__":
    sample_properties = [
        Property(name="Marina Loft", area="Dubai Marina", price=1_200_000, monthly_rent=7500, size_sqft=850),
        Property(name="DIP Villa", area="DIP", price=2_400_000, monthly_rent=13000, size_sqft=2200),
        Property(name="South Studio", area="Dubai South", price=650_000, monthly_rent=4500, size_sqft=480),
        Property(name="Downtown Apt", area="Downtown Dubai", price=1_800_000, monthly_rent=9000, size_sqft=1000),
    ]

    ranked = rank_properties(sample_properties, years=5, appreciation_pct=3.0)
    print_report(ranked, years=5)
