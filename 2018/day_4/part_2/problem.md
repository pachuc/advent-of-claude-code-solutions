# Problem Report: Guard Sleep Pattern Analysis - Part 2

## Objective
Using the same guard sleep pattern data from Part 1, implement a different strategy to identify the optimal guard/minute combination. Instead of finding the sleepiest guard overall, find the guard who is most consistently asleep at the same specific minute.

## Context from Part 1
Guards work overnight shifts at a manufacturing lab. Historical observations show when guards fall asleep and wake up during their shifts. All sleep/wake events occur during the midnight hour (00:00 - 00:59).

In Part 1, we used **Strategy 1**: Find the guard with the most total sleep minutes, then find which minute that guard sleeps most frequently. This yielded answer **48680**.

## Part 2 Strategy Change
**Strategy 2:** Of all guards and all minutes, find which specific guard is most frequently asleep on the same minute. In other words, find the (guard, minute) pair with the highest frequency count.

## Input Format
The input is the same as Part 1:
- Timestamped records (not in chronological order)
- Three event types:
  1. `Guard #<ID> begins shift` - A guard starts their shift
  2. `falls asleep` - The current guard falls asleep
  3. `wakes up` - The current guard wakes up

**Important Notes:**
- Records must be sorted chronologically first
- Guards count as asleep on the minute they fall asleep
- Guards count as awake on the minute they wake up (not asleep on wake-up minute)
- All sleep/wake events occur during the midnight hour (00:00 - 00:59)

## Expected Output
The answer should be: **Guard ID × Minute**

Where:
- **Guard ID** is the ID of the guard who is most frequently asleep at a specific minute
- **Minute** is the specific minute (0-59) where this guard is most frequently asleep

The key difference from Part 1: We're not looking for the guard with the most total sleep, but rather the guard-minute pair with the highest consistency/frequency.

## Example
Using the same sample data from Part 1:
- Guard #10 was asleep at minute 24 twice
- Guard #99 was asleep at minute 45 **three times**
- All other (guard, minute) combinations occurred at most twice
- Therefore, Guard #99 at minute 45 is the most frequent combination
- Answer: 99 × 45 = **4455**

## Processing Steps Required
1. Parse all input records and extract timestamps and events (same as Part 1)
2. Sort records chronologically by timestamp (same as Part 1)
3. Associate each sleep/wake event with the correct guard (same as Part 1)
4. For each guard, track all minutes they were asleep across all shifts (same as Part 1)
5. **NEW:** Across ALL guards and ALL minutes (0-59), find the single (guard, minute) pair with the highest frequency count
6. Calculate and return: Guard ID × Minute

## Key Difference from Part 1
Part 1: Find sleepiest guard → then find that guard's most frequent minute
Part 2: Find the (guard, minute) pair with highest frequency across ALL guards and minutes simultaneously
