# Problem Report: Guard Sleep Pattern Analysis

## Objective
Determine which guard is most likely to be asleep at a specific time by analyzing historical sleep patterns from guard shift records. The goal is to identify the optimal guard/minute combination to maximize the chance of sneaking past the guard post.

## Context
Guards work overnight shifts at a manufacturing lab. Historical observations have been recorded showing when guards fall asleep and wake up during their shifts. All sleep/wake events occur during the midnight hour (00:00 - 00:59), so only the minute portion (00-59) is relevant for analysis.

## Input Format
The input consists of timestamped records in chronological disorder. Each line contains:
- A timestamp in format: `[YYYY-MM-DD HH:MM]`
- An event description, which can be one of three types:
  1. `Guard #<ID> begins shift` - A guard with the given ID starts their shift
  2. `falls asleep` - The current guard falls asleep
  3. `wakes up` - The current guard wakes up

**Important Notes:**
- Records are NOT in chronological order and must be sorted first
- The guard falling asleep or waking up is always the one whose shift most recently started
- Guards count as asleep on the minute they fall asleep
- Guards count as awake on the minute they wake up (not asleep on wake-up minute)
- All sleep/wake events occur during the midnight hour (00:00 - 00:59)

## Strategy to Solve
**Strategy 1:** Find the guard that has the most total minutes asleep across all their shifts. Then determine which specific minute (0-59) that guard spends asleep most frequently.

## Expected Output
The answer should be: **Guard ID × Minute**

Where:
- **Guard ID** is the ID number of the guard who has the most total minutes asleep
- **Minute** is the specific minute (0-59) during which that guard is asleep most frequently across all their shifts

## Example
Given the sample data:
- Guard #10 slept for 50 total minutes (20+25+5 across three shifts)
- Guard #99 slept for 30 total minutes (10+10+10 across three shifts)
- Guard #10 is the sleepiest guard
- Guard #10 was asleep most during minute 24 (asleep during minute 24 on two different days)
- Answer: 10 × 24 = **240**

## Processing Steps Required
1. Parse all input records and extract timestamps and events
2. Sort records chronologically by timestamp
3. Associate each sleep/wake event with the correct guard (the one whose shift most recently started)
4. For each guard, track all minutes they were asleep across all shifts
5. Calculate total minutes asleep for each guard
6. Identify the guard with the most total minutes asleep
7. For that guard, determine which minute (0-59) they were asleep most frequently
8. Calculate and return: Guard ID × Minute
