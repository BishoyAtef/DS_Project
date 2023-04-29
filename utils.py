"""utility functions for data cleaning"""
from typing import List, Tuple
import numpy as np

def get_outliers(nums: List[float], use_iqd: bool = True)-> Tuple[List[int], List[float]]:
    """
    Returns a list of outliers and their indexes in the given list of numbers
    """
    outlier_indecies: List[int] = []
    outlier_values: List[float] = []
    if use_iqd:
        # compute the interquartile range
        q_1: float = float(np.percentile(nums, 25))
        q_3: float = float(np.percentile(nums, 75))
        iqr: float = q_3 - q_1
        # compute the lower and upper bounds
        lower_bound: float = q_1 - (1.5 * iqr)
        upper_bound: float = q_3 + (1.5 * iqr)
        # find the outliers
        for index, num in enumerate(nums):
            if num < lower_bound or num > upper_bound:
                outlier_indecies.append(index)
                outlier_values.append(num)
    else:
        # cast to float beacuse the return type is floating[any]
        mean: float = float(np.mean(nums))
        std: float = float(np.std(nums))
        for index, num in enumerate(nums):
            z_score: float = (num - mean) / std
            if np.abs(z_score) > 3:
                outlier_indecies.append(index)
                outlier_values.append(num)
    return outlier_indecies, outlier_values

def substitute_outliers_with_mean(nums: List[float], outlier_indexes:List[int])->List[float]:
    """return a list of numbers with outliers replaced by the median"""
    # replace the outliers with the median
    median: float = float(np.median(nums))
    for index in outlier_indexes:
        nums[index] = median
    return nums
    # mean: float = float(np.mean(nums))
    # for index in outlier_indexes:
    #     nums[index] = mean
    # return nums

def numbers_datacleaning_pipe(nums: List[float])->List[float]:
    """returns a list of numbers with outliers replaced by the mean"""
    outlier_indexes, _ = get_outliers(nums)
    # if there are no outliers, return the original list
    if len(outlier_indexes) == 0:
        print("No outliers found")
        return nums
    else:
        print(f"Found {len(outlier_indexes)} outliers")
        return substitute_outliers_with_mean(nums, outlier_indexes)
