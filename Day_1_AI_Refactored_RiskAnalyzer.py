from typing import Tuple
import math


class RiskAnalyzer:
    """
    A professional risk analysis class for financial time series data.
    
    This class provides methods to calculate volatility and compare risk metrics
    across different time periods using daily returns data.
    
    Attributes:
        daily_returns (Tuple[float, ...]): Immutable tuple of daily return percentages
    """
    
    def __init__(self, daily_returns: Tuple[float, ...]) -> None:
        """
        Initialize the RiskAnalyzer with daily returns data.
        
        Args:
            daily_returns: Tuple of daily return percentages
            
        Raises:
            ValueError: If daily_returns is empty or contains non-numeric values
        """
        if not daily_returns:
            raise ValueError("Daily returns cannot be empty")
        
        if not all(isinstance(x, (int, float)) for x in daily_returns):
            raise ValueError("All returns must be numeric values")
            
        self.daily_returns: Tuple[float, ...] = daily_returns
    
    def calculate_volatility(self, returns: Tuple[float, ...] = None) -> float:
        """
        Calculate the volatility (standard deviation) of returns.
        
        Volatility is computed as the square root of the variance,
        using the population standard deviation formula.
        
        Args:
            returns: Optional tuple of returns. If None, uses instance daily_returns
            
        Returns:
            The volatility (standard deviation) as a float
        """
        if returns is None:
            returns = self.daily_returns
        
        n: int = len(returns)
        mean: float = sum(returns) / n
        squared_diff: list[float] = [(x - mean) ** 2 for x in returns]
        variance: float = sum(squared_diff) / n
        volatility: float = math.sqrt(variance)
        
        return volatility
    
    def split_period(self) -> Tuple[Tuple[float, ...], Tuple[float, ...]]:
        """
        Split the daily returns into two equal halves.
        
        Returns:
            A tuple containing (first_half, second_half) of returns
        """
        midpoint: int = len(self.daily_returns) // 2
        first_half: Tuple[float, ...] = self.daily_returns[:midpoint]
        second_half: Tuple[float, ...] = self.daily_returns[midpoint:]
        
        return first_half, second_half
    
    def compare_period_volatility(self) -> dict[str, float]:
        """
        Compare volatility between the first and second half of the period.
        
        Returns:
            Dictionary containing:
                - first_period_volatility: Volatility of first half
                - second_period_volatility: Volatility of second half
                - volatility_change: Absolute change in volatility
                - volatility_change_percent: Percentage change in volatility
        """
        first_half, second_half = self.split_period()
        
        vol_first: float = self.calculate_volatility(first_half)
        vol_second: float = self.calculate_volatility(second_half)
        vol_change: float = vol_second - vol_first
        vol_change_pct: float = (vol_change / vol_first) * 100
        
        return {
            'first_period_volatility': vol_first,
            'second_period_volatility': vol_second,
            'volatility_change': vol_change,
            'volatility_change_percent': vol_change_pct
        }
    
    def get_summary_statistics(self) -> dict[str, float]:
        """
        Calculate comprehensive summary statistics for the returns.
        
        Returns:
            Dictionary containing mean, volatility, min, max, and count
        """
        return {
            'mean': sum(self.daily_returns) / len(self.daily_returns),
            'volatility': self.calculate_volatility(),
            'min': min(self.daily_returns),
            'max': max(self.daily_returns),
            'count': len(self.daily_returns)
        }
    
    def __repr__(self) -> str:
        """String representation of the RiskAnalyzer instance."""
        return f"RiskAnalyzer(n_observations={len(self.daily_returns)})"
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        stats = self.get_summary_statistics()
        return (f"RiskAnalyzer with {stats['count']} observations\n"
                f"Mean: {stats['mean']:.4f}, Volatility: {stats['volatility']:.4f}")


# Example Usage
if __name__ == "__main__":
    # Define returns as immutable tuple
    daily_returns: Tuple[float, ...] = (
        1.22, 1.29, 2.24, 3.32, 4.25, 8.25, 6.25, 5.25, 4.36, 9.25,
        7.82, 6.29, 4.12, 8.35, 1.95, 6.23, 1.42, 10.00, 9.95, 10.25
    )
    
    # Initialize analyzer
    analyzer = RiskAnalyzer(daily_returns)
    print(analyzer)
    print("\n" + "="*50 + "\n")
    
    # Calculate overall volatility
    overall_vol = analyzer.calculate_volatility()
    print(f"Overall Volatility: {overall_vol:.4f}")
    print()
    
    # Compare period volatility
    comparison = analyzer.compare_period_volatility()
    print("Period Comparison:")
    print(f"  First 10 Days Volatility:  {comparison['first_period_volatility']:.4f}")
    print(f"  Last 10 Days Volatility:   {comparison['second_period_volatility']:.4f}")
    print(f"  Absolute Change:           {comparison['volatility_change']:+.4f}")
    print(f"  Percentage Change:         {comparison['volatility_change_percent']:+.2f}%")
    print()
    
    # Summary statistics
    stats = analyzer.get_summary_statistics()
    print("Summary Statistics:")
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title():20s}: {value:.4f}")
