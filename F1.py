import random

def simulate_race(drivers, track, weather, laps):
    """Simulates an F1 race with lap-by-lap events and returns results."""
    race_results = []
    incidents = []
    lap_events = []
    base_time = 90 * laps  # Base total race time in seconds
    
    # Determine weather condition
    weather_condition = random.choices(['Dry', 'Light Rain', 'Heavy Rain'], 
                                     weights=[0.7, 0.2, 0.1])[0]
    wet_track = weather_condition != 'Dry'
    
    active_drivers = drivers.copy()  # Track drivers who haven't DNF'd
    
    for driver in drivers:
        # 5% chance of DNF (Did Not Finish)
        if random.random() < 0.05:
            incidents.append(f"{driver['name']} - DNF (Mechanical Failure)")
            active_drivers.remove(driver)
            continue
        
        # Performance factors
        base_speed = driver['skill'] * random.uniform(0.9, 1.1)
        car_performance = driver['car'] * random.uniform(0.95, 1.05)
        track_factor = track['difficulty'] * random.uniform(0.9, 1.1)
        weather_factor = weather * random.uniform(0.85, 1.15)
        
        # Tire strategy
        if wet_track:
            tire_choice = random.choice(['intermediate', 'wet'])
        else:
            tire_choice = random.choice(['soft', 'medium', 'hard'])
        
        tire_strategies = {'soft': 1.05, 'medium': 1.00, 'hard': 0.95, 
                          'intermediate': 0.90, 'wet': 0.85}
        
        # Pit stop time (random impact)
        pit_stop_penalty = random.uniform(1, 5)
        
        # Historical performance adjustment
        historical_factor = driver.get('history', 1.0) * random.uniform(0.95, 1.05)
        
        # Penalties with specific reasons
        penalty_time = 0
        if random.random() < 0.1:  # 10% chance of penalty
            penalty_type = random.choices(
                ['Track Limits', 'Unsafe Release', 'Collision', 'Overtaking Under SC', 'Ignoring Blue Flags'],
                weights=[0.4, 0.2, 0.2, 0.1, 0.1]
            )[0]
            
            if penalty_type == 'Track Limits':
                penalty_time = random.choice([5, 10])
                incidents.append(f"{driver['name']} - {penalty_time}s penalty ({penalty_type} - Repeated violations)")
            elif penalty_type == 'Unsafe Release':
                penalty_time = random.choice([5, 10])
                incidents.append(f"{driver['name']} - {penalty_time}s penalty ({penalty_type} - Dangerous pit exit)")
            elif penalty_type == 'Collision':
                penalty_time = random.choice([5, 10, 15])
                other_driver = random.choice([d for d in drivers if d['name'] != driver['name']])
                incidents.append(f"{driver['name']} - {penalty_time}s penalty ({penalty_type} - Caused collision with {other_driver['name']})")
            elif penalty_type == 'Overtaking Under SC':
                penalty_time = 10
                incidents.append(f"{driver['name']} - {penalty_time}s penalty ({penalty_type} - Gained advantage under Safety Car)")
            elif penalty_type == 'Ignoring Blue Flags':
                penalty_time = 5
                incidents.append(f"{driver['name']} - {penalty_time}s penalty ({penalty_type} - Failed to let leaders through)")
        
        # Calculate total performance
        total_performance = (base_speed + car_performance + track_factor + weather_factor) * \
                           tire_strategies[tire_choice] - pit_stop_penalty * historical_factor
        
        # Calculate total race time
        total_time = base_time / (total_performance / 100) + penalty_time
        
        race_results.append((driver['name'], total_time, penalty_time, tire_choice))

    # Generate lap events
    for lap in range(1, laps + 1):
        event_chance = random.random()
        if event_chance < 0.05:
            lap_events.append(f"Lap {lap}: Safety Car Deployed!")
        elif event_chance < 0.10 and active_drivers:  # Only if there are active drivers left
            retired_driver = random.choice(active_drivers)
            incidents.append(f"{retired_driver['name']} - DNF (Crash)")
            lap_events.append(f"Lap {lap}: {retired_driver['name']} crashes out!")
            active_drivers.remove(retired_driver)
            # Remove from race results too
            race_results = [r for r in race_results if r[0] != retired_driver['name']]

    
    # Sort results by race time
    race_results.sort(key=lambda x: x[1])
    
    # Ensure Nico Hulkenberg never finishes in the top 3
    for i, (name, _, _, _) in enumerate(race_results[:3]):
        if name == "Nico Hulkenberg":
            if len(race_results) > 3:  # Only swap if there are enough drivers
                swap_index = random.randint(3, len(race_results) - 1)
                race_results[i], race_results[swap_index] = race_results[swap_index], race_results[i]
    
    # Calculate time gaps
    if race_results:  # Only if there are results
        winner_time = race_results[0][1]
        final_results = []
        for name, time, penalty, tires in race_results:
            time_gap = round(time - winner_time, 2)
            final_results.append((name, time_gap, penalty, tires))
    else:
        final_results = []
    
    return weather_condition, lap_events, final_results, incidents

# 2025 F1 Calendar with track difficulties
tracks = [
    {'name': 'Bahrain GP', 'difficulty': 90},
    {'name': 'Saudi Arabian GP', 'difficulty': 88},
    {'name': 'Australian GP', 'difficulty': 85},
    {'name': 'Japanese GP', 'difficulty': 92},
    {'name': 'Chinese GP', 'difficulty': 87},
    {'name': 'Miami GP', 'difficulty': 89},
    {'name': 'Spanish GP', 'difficulty': 91},
    {'name': 'Monaco GP', 'difficulty': 95},
    {'name': 'Canadian GP', 'difficulty': 86},
    {'name': 'Austrian GP', 'difficulty': 89},
    {'name': 'British GP', 'difficulty': 93},
    {'name': 'Hungarian GP', 'difficulty': 88},
    {'name': 'Belgian GP', 'difficulty': 94},
    {'name': 'Dutch GP', 'difficulty': 90},
    {'name': 'Italian GP', 'difficulty': 89},
    {'name': 'Azerbaijan GP', 'difficulty': 87},
    {'name': 'Singapore GP', 'difficulty': 95},
    {'name': 'United States GP', 'difficulty': 92},
    {'name': 'Mexican GP', 'difficulty': 91},
    {'name': 'Brazilian GP', 'difficulty': 93},
    {'name': 'Las Vegas GP', 'difficulty': 90},
    {'name': 'Abu Dhabi GP', 'difficulty': 92}
]

# Points system (top 10)
points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

# Driver database with skill, car performance, and historical factors
drivers = [
    {'name': 'Max Verstappen', 'skill': 98, 'car': 95, 'history': 1.05},
    {'name': 'Sergio Perez', 'skill': 92, 'car': 95, 'history': 1.02},
    {'name': 'Lewis Hamilton', 'skill': 97, 'car': 92, 'history': 1.08},
    {'name': 'George Russell', 'skill': 94, 'car': 92, 'history': 1.03},
    {'name': 'Charles Leclerc', 'skill': 95, 'car': 91, 'history': 1.02},
    {'name': 'Carlos Sainz', 'skill': 94, 'car': 91, 'history': 1.02},
    {'name': 'Lando Norris', 'skill': 93, 'car': 89, 'history': 1.01},
    {'name': 'Oscar Piastri', 'skill': 91, 'car': 89, 'history': 1.00},
    {'name': 'Fernando Alonso', 'skill': 94, 'car': 88, 'history': 1.04},
    {'name': 'Lance Stroll', 'skill': 80, 'car': 88, 'history': 0.10},
    {'name': 'Pierre Gasly', 'skill': 90, 'car': 87, 'history': 0.99},
    {'name': 'Esteban Ocon', 'skill': 90, 'car': 87, 'history': 0.99},
    {'name': 'Yuki Tsunoda', 'skill': 88, 'car': 85, 'history': 0.97},
    {'name': 'Daniel Ricciardo', 'skill': 100, 'car': 100, 'history': 1.10},
    {'name': 'Valtteri Bottas', 'skill': 89, 'car': 84, 'history': 0.96},
    {'name': 'Zhou Guanyu', 'skill': 86, 'car': 84, 'history': 0.95},
    {'name': 'Kevin Magnussen', 'skill': 87, 'car': 83, 'history': 0.94},
    {'name': 'Nico Hulkenberg', 'skill': 88, 'car': 83, 'history': 0.95},
    {'name': 'Alex Albon', 'skill': 90, 'car': 82, 'history': 0.96},
    {'name': 'Logan Sargeant', 'skill': 85, 'car': 82, 'history': 0.93}
]

# Initialize championship standings
championship = {driver['name']: 0 for driver in drivers}
wins = {driver['name']: 0 for driver in drivers}
podiums = {driver['name']: 0 for driver in drivers}
fastest_laps = {driver['name']: 0 for driver in drivers}

# Simulate the full championship
for track in tracks:
    laps = random.randint(50, 70)
    weather = 100 if track['name'] in ['Bahrain GP', 'Miami GP', 'Saudi Arabian GP', 
                                     'Azerbaijan GP', 'Abu Dhabi GP', 'Mexican GP'] else random.uniform(70, 100)
    
    weather_condition, lap_events, race_results, incidents = simulate_race(drivers, track, weather, laps)
    
    print(f"\n🏁 {track['name']} ({weather_condition} Conditions, {laps} laps)")
    print("=" * 50)
    
    # Print lap events
    if lap_events:
        print("\nRace Events:")
        for event in lap_events:
            print(f"⚡ {event}")
    
    # Print incidents
    if incidents:
        print("\nIncidents:")
        for incident in incidents:
            print(f"⚠️ {incident}")
    
    # Print race results - only if we have results
    if race_results:
        print("\nRace Results:")
        for position, (driver, time_gap, penalty, tires) in enumerate(race_results, start=1):
            penalty_text = f" [Penalty: +{penalty}s]" if penalty > 0 else ""
            print(f"{position}. {driver} (+{time_gap}s){penalty_text} ({tires} tires)")
        
        # Assign points and statistics only if we have results
        for i, (driver, _, _, _) in enumerate(race_results[:10]):
            championship[driver] += points[i]
            if i == 0:
                wins[driver] += 1
            if i < 3:
                podiums[driver] += 1
            if i == 0 and random.random() < 0.5:  # 50% chance race winner gets fastest lap
                fastest_laps[driver] += 1
            elif i < 10 and random.random() < 0.1:  # 10% chance for others in top 10
                fastest_laps[driver] += 1
    else:
        print("\nRace Results: No finishers!")

# Print final championship standings
print("\n🏆 2025 FIA Formula 1 World Championship Final Standings 🏆")
print("=" * 70)
sorted_standings = sorted(championship.items(), key=lambda x: x[1], reverse=True)
for position, (driver, score) in enumerate(sorted_standings, start=1):
    print(f"{position}. {driver:20} {score:3} pts | Wins: {wins[driver]} | Podiums: {podiums[driver]} | Fastest Laps: {fastest_laps[driver]}")
