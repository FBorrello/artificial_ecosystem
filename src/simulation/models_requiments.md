# Models Module (`models.py`) Requirements

## Overview

The `models.py` module will define the core entities and their behaviors within the artificial ecosystem,
including fish, plants, and possibly environmental factors. This document outlines the general requirements
for the models to ensure they interact realistically and efficiently within the ecosystem simulation.

## Requirements

### 1. **Entity Classes**
   - **Fish Class**: Must include attributes for species, size, health, age, and behavior (e.g., schooling, predatory).
   - **Plant Class**: Should have attributes for species, growth rate, nutrient requirements, and environmental
   impact (e.g., oxygen production, habitat provision).
   - **Environment Class**: Represents the ecosystem's environment, including water quality, light levels,
   temperature, and nutrient distribution.

### 2. **Interactions**
   - **Predator-Prey Dynamics**: Implement methods to simulate predation, including hunting strategies,
   escape responses, and population dynamics.
   - **Competition for Resources**: Define how entities compete for nutrients, space, and light, influencing
   growth and survival rates.
   - **Symbiotic Relationships**: Model mutualistic or commensal interactions where one or both entities benefit
   without harm to the other.

### 3. **Growth and Development**
   - **Life Cycle Modeling**: Include stages like birth, growth, reproduction, and death. Each stage should affect
   other attributes like size, health, and behavior.
   - **Ageing and Mortality**: Entities should age over time, with age affecting their capabilities and likelihood
   of death from natural causes or predation.

### 4. **Environmental Impact**
   - **Nutrient Cycle**: Model how nutrients are absorbed by plants, transferred through the food chain, and recycled
   back into the environment.
   - **Environmental Changes**: The model should reflect changes in environmental conditions and how these affect the
   ecosystem's entities.

### 5. **Behavioral Complexity**
   - **Adaptive Behaviors**: Entities should adapt their behavior based on environmental conditions and interactions
   with other entities.
   - **Learning and Evolution**: Over time, behaviors should evolve