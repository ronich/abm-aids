
# coding: utf-8

# # Zajęcia 5
# 
# ###[Przykład 2](http://simpy.readthedocs.org/en/latest/examples/gas_station_refuel.html)
# Covers:
# 
# - Resources: Resource
# - Resources: Container
# - Waiting for other processes
# 
# This examples models a gas station and cars that arrive at the station for refueling.
# 
# The gas station has a limited number of fuel pumps and a fuel tank that is shared between the fuel pumps. The gas station is thus modeled as Resource. The shared fuel tank is modeled with a Container.
# 
# Vehicles arriving at the gas station first request a fuel pump from the station. Once they acquire one, they try to take the desired amount of fuel from the fuel pump. They leave when they are done.
# 
# The gas stations fuel level is reqularly monitored by gas station control. When the level drops below a certain threshold, a tank truck is called to refuel the gas station itself.

# W przykładzie wystepują 3 typy agentów:
# - samochody reprezentowane przez obiekty klasy `simpy.Process`, ktorych zachowanie opisuje funkcja `car()`. Samochody przyjeżdżają na stację benzynową żeby zatankować paliwo
# - stacja benzynowa reprezentowana przez obiekt klasy `simpy.Process`, ktorej zachowanie opisuje funkcja `gas_station_control()`. Stacja benzynowa ma okresloną liczbę dystrybutorów paliwa, reprezentowanych przez obiekt klasy `simpy.Resource` oraz ograniczony zapas paliwa reprezentowany przez obiekt klasy `simpy.Container`. Obsluga stacji okresowo sprawdza stan paliwa w zbiorniku, i jesli spadnie on ponizej okreslonego progu (`THRESHOLD`), zamawia dostawę w celu uzupełnienia zasobu.
# - samochód-cysterna z paliwem, uzupelniajacy zapasy stacji, reprezentowany przez obiekt klasy `simpy.Process`, którego zachowanie opisuje funkcja `tank_truck()`.
# 
# Przebieg symulacji jest sterowany przez strumień samochodów, generowany przez funkcję `car_generator()`.
# 
# Nowym elementem wprowadzonym w symulacji jest zapas paliwa o ograniczonej pojemności reprezentowany przez obiekt klasy `simpy.Container`. Obiekt tej klasy pozwala na pobieranie (tankowanie) zasobu metodą `get()` oraz uzupełnianie zużytego zapasu metodą `put()`.

# In[12]:

"""
Gas Station Refueling example

Covers:

- Resources: Resource
- Resources: Container
- Waiting for other processes

Scenario:
  A gas station has a limited number of gas pumps that share a common
  fuel reservoir. Cars randomly arrive at the gas station, request one
  of the fuel pumps and start refueling from that reservoir.

  A gas station control process observes the gas station's fuel level
  and calls a tank truck for refueling if the station's level drops
  below a threshold.

"""
import random
import simpy


RANDOM_SEED = 42
GAS_STATION_SIZE = 200     # liters
THRESHOLD = 10             # Threshold for calling the tank truck (in %)
FUEL_TANK_SIZE = 50        # liters
FUEL_TANK_LEVEL = [5, 25]  # Min/max levels of fuel tanks (in liters)
REFUELING_SPEED = 2        # liters / second
TANK_TRUCK_TIME = 300      # Seconds it takes the tank truck to arrive
T_INTER = [30, 300]        # Create a car every [min, max] seconds
SIM_TIME = 1000            # Simulation time in seconds


def car(name, env, gas_station, fuel_pump):
    """A car arrives at the gas station for refueling.

    It requests one of the gas station's fuel pumps and tries to get the
    desired amount of gas from it. If the stations reservoir is
    depleted, the car has to wait for the tank truck to arrive.

    """
    fuel_tank_level = random.randint(*FUEL_TANK_LEVEL)
    print('%s arriving at gas station at %.1f' % (name, env.now))
    with gas_station.request() as req:
        start = env.now
        # Request one of the gas pumps
        yield req

        # Get the required amount of fuel
        liters_required = FUEL_TANK_SIZE - fuel_tank_level
        yield fuel_pump.get(liters_required)

        # The "actual" refueling process takes some time
        yield env.timeout(liters_required / REFUELING_SPEED)

        print('%s finished refueling in %.1f seconds.' % (name,
                                                          env.now - start))


def gas_station_control(env, fuel_pump):
    """Periodically check the level of the *fuel_pump* and call the tank
    truck if the level falls below a threshold."""
    while True:
        if fuel_pump.level / fuel_pump.capacity * 100 < THRESHOLD:
            # We need to call the tank truck now!
            print('Calling tank truck at %d' % env.now)
            # Wait for the tank truck to arrive and refuel the station
            yield env.process(tank_truck(env, fuel_pump))

        yield env.timeout(10)  # Check every 10 seconds


def tank_truck(env, fuel_pump):
    """Arrives at the gas station after a certain delay and refuels it."""
    yield env.timeout(TANK_TRUCK_TIME)
    print('Tank truck arriving at time %d' % env.now)
    amount = fuel_pump.capacity - fuel_pump.level
    print('Tank truck refuelling %.1f liters.' % amount)
    yield fuel_pump.put(amount)


def car_generator(env, gas_station, fuel_pump):
    """Generate new cars that arrive at the gas sbtation."""
    i = 1
    while True:
        yield env.timeout(random.randint(*T_INTER))
        env.process(car('Car %d' % i, env, gas_station, fuel_pump))
        i += 1


# Setup and start the simulation
print('Gas Station refuelling')
random.seed(RANDOM_SEED)


# In[13]:

# Create environment and start processes
env = simpy.Environment()
gas_station = simpy.Resource(env, 2)
fuel_pump = simpy.Container(env, GAS_STATION_SIZE, init=GAS_STATION_SIZE)
env.process(gas_station_control(env, fuel_pump))
env.process(car_generator(env, gas_station, fuel_pump))

# Execute!
env.run(until=SIM_TIME)

