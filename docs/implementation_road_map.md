# Artificial Ecosystem Project Development Roadmap

### Legend.
- [ ] Pending
- [X] Completed

## Phase 1: Foundation and Core Setup

### Increment 1-2: Project Setup and Initial Documentation 
- [X] Setup version control (Git), create the project structure, and write initial README.md with setup instructions.

### Increment 3-4: Basic Simulation Framework 
- [X] Development of basic simulation logic in simulation/models.py for core components like fish, plants, and environment.
- [ ] Initial setup of visualization tools in simulation/visualization.py.
- [ ] Add Docker support with Dockerfile for simulation and hardware environments.

## Phase 2: Simulation Refinement and Hardware Integration

### Increment 5-6: Advanced Simulation Features 
- [ ] Enhance simulation with more complex behaviors, interactions, and environmental factors.
- [ ] Add CLI-based mode switching via main.py using arguments --mode=simulation or --mode=hardware.
- [ ] Implement simulated sensors and actuators logic in simulation/sensors.py and simulation/actuators.py.

### Increment 7-8: Hardware Interface Development 
- [ ] Start developing real-world interaction modules in hardware/.
- [ ] Update hardware/ for better scalability, including handling of more sensors or actuators.
- [ ] Integration of actual sensors and actuators in hardware/sensors.py and hardware/actuators.py.

## Phase 3: Core System Logic

### Increment 9-10: Ecosystem Logic Integration 
- [ ] Develop core ecosystem logic that can operate both in simulation and real-world scenarios in common/ecosystem.py.
- [ ] Ensure the logic can handle inputs from both simulated and real sensors.

## Phase 4: User Interface Development

### Increment 11-12: Web Interface Setup 
- [ ] Begin development of the web interface using Flask or Django in web/.
- [ ] Setup basic templates for user interaction in web/templates/.
- [ ] Add monitoring integration in setup with external tools like Prometheus or Grafana.

### Increment 13-14: Web Interface Features 
- [ ] Implement features like real-time data viewing, control interfaces for actuators, and simulation control.

## Phase 5: Testing and Documentation

### Increment 15-16: Unit Testing and Integration Testing 
- [ ] Develop unit tests for individual components in tests/.
- [ ] Define CI/CD pipeline with automated testing and deployment workflows under ci_cd/.
- [ ] Perform integration testing to ensure all parts work together as expected.

### Increment 17-18: Documentation and User Guides 
- [ ] Enhance documentation in docs/, including setup guides and API documentation if applicable.
- [ ] Add details on running simulation and hardware with Docker to docs/setup_guide.md.
- [ ] Create user manuals or guides for how to operate the system in both simulation and real-world scenarios.

## Phase 6: Final Integration and Optimization

### Increment 19-20: Final Integration 
- [ ] Ensure all components (simulation, hardware, web interface) are fully integrated.
- [ ] Add log-rotation mechanism for long-term use in data/logs.
- [ ] Perform system-wide testing, focusing on performance, reliability, and accuracy.

### Increment 21-22: Optimization and Bug Fixing 
- [ ] Optimize code for performance, especially in simulation algorithms and real-time data processing.
- [ ] Fix any bugs reported during integration testing.

## Phase 7: Deployment and Maintenance

### Increment 23-24: Deployment 
- [ ] Define project requirements in requirements.txt and setup.py.
- [ ] Deploy the system to a production environment or prepare for real-world deployment if hardware is involved.
- [ ] Setup any necessary backend services, databases, or cloud infrastructure.
- [ ] Ongoing: Maintenance and Updates
- [ ] Regular updates based on user feedback, bug reports, or changes in technology or requirements.


# 2025-01-01

### **Current Architecture Review**
#### **Strengths**:
- Added Dockerfile simplifies setup for simulation and hardware environments.
#### **Strengths**:
1. **Clear Separation of Concerns**:
    - Simulation (`src/simulation/`) and real-world hardware code (`src/hardware/`) are separated, ensuring flexibility and facilitating testing.
    - Shared logic in `src/common/` reduces code duplication, allowing for easier updates to core behavior.

2. **Configurability**:
    - Using configurations (`config/`) for simulation and hardware provides adaptability without code manipulation.
    - YAML and JSON formats are developer-friendly and support dynamic loading.

3. **Testing**:
    - Tests are well-segregated (`tests/`) and likely cover both simulation and hardware interactions.
3. **Testing**:
- Defines CI/CD pipelines with automated workflows in ci_cd/.
4. **Extendability**:
    - Inclusion of a `web/` folder (Flask/Django) allows for future expansions toward a GUI for monitoring or debugging.

5. **Documentation**:
- Updated docs/setup_guide.md with instructions for Docker usage.
    - Guides in `docs/` for setup and APIs ensure new developers or users can get started easily.

6. **Environment Transition**:
    - Thoughtful implementation of configuration management and modularity ensures an easier transition from simulation to real-world application.

#### **Opportunities for Improvement**:
1. **Containerization**:
    - Adding Docker configurations or similar containerization can ensure the environment (simulation vs. real-world) is consistent, especially when other team members or users run it in varying environments.

2. **Scalability**:
    - The current structure works well for a small-scale simulation or application, but as components grow (e.g., more sensors, distributed systems), refactoring for scalability may be required. Adopting a microservices approach for hardware modules or a message-broker-based communication system can aid this.

3. **Monitoring and Debugging Tools**:
3. **Monitoring and Debugging Tools**:
- Incorporated external monitoring with tools like Prometheus, Grafana.

4. **Unit Tests Coverage**:
    - Ensure each layer (e.g., actuators, sensors, ecosystem logic, visualization) is rigorously unit-tested to handle edge cases.

5. **DevOps Enhancements**:
    - Setting up CI/CD pipelines to automatically test key functions, ensure style compliance, and validate deployments.

### **Updated Roadmap**
- Containerization is introduced for standardizing simulation and hardware environments.
Here’s an updated roadmap considering the current implementation, identifying possible extensions, and integrating suggestions:
#### **Phase 1: Complete Core Testing**
- Finalize unit and integration tests in the `tests/` directory.
- Add CI/CD pipelines for automated tests and deployments under ci_cd/.
- Ensure test coverage across shared ecosystem logic (`ecosystem.py`) and hardware interactions (`hardware_interface.py`).

#### **Phase 2: Enhancements to Configurations**
- Develop a unified configuration loader capable of:
    - Dynamically switching between `simulation_config.yml` and `hardware_config.yml`.
    - Validating configuration schema (using `pydantic` or similar libraries).

- Allow command-line arguments in `main.py` for runtime configuration (e.g., `--mode=simulation` or `--mode=hardware`).

#### **Phase 3: Refactor Ecosystem Logic if Needed**
- Evaluate the `ecosystem.py` file for scalability when handling complex ecosystems (e.g., higher entities like predators or plants' growth patterns over time).
- Modularize components further if needed (e.g., splitting ecosystem logic by entity type like Fish, Plants).

#### **Phase 4: Visualization Improvements**
- Render real-time insights from both simulation and real-world scenarios in the `visualization.py` module.
- Extend `web/app.py` to create a dashboard with:
    - Environmental state monitoring.
    - Fish/plant status updates.
    - Actuator control states (e.g., whether a pump or motor is active).

#### **Phase 5: Transition to Real-World Integration**
- Finalize the `hardware_interface.py` module:
    - Ensure synchronization between hardware/sensor inputs and core `ecosystem.py`.
    - Validate real-world calibration scenarios against `calibration_data.json`.
- Improve readiness for scaling up hardware devices (e.g., managing multiple sensors).

#### **Phase 6: Deployment Preparedness**
- Add Docker support to simplify running the ecosystem for both simulation and hardware environments.
- Add deployment infrastructure for the web application (e.g., Flask app hosted on AWS, Azure, or Heroku).

#### **Phase 7: Extend Ecosystem Dynamics**
- Simulate more complex ecosystem behaviors (e.g., interaction between fish species, climate variability, water temperature changes, etc.).
- Introduce real-time AI-driven adjustments for ecosystem balance (e.g., adjusting parameters to stabilize plant growth or fish populations).

#### **Phase 8: Long-term Scalability**
- Introduce the possibility of distributed simulation (e.g., using Python’s multiprocessing or task queues like Celery).
- Set up inter-process communication (IPC) between hardware modules (e.g., sensors and actuators) using libraries like ZeroMQ or an MQTT broker.

### **Next Steps**
Based on this review and revised roadmap, here’s what can be prioritized immediately:
1. **Finalize Ecosystem Logic**:
    - Verify and finalize the logic in `ecosystem.py`.
    - Ensure the existing logic can seamlessly switch between simulated and hardware-based environments.

2. **Unit Testing Improvements**:
    - Expand test coverage for critical components in both `simulation/` and `hardware/`.

3. **Streamline Configuration Management**:
    - Build a unified configuration loader.
    - Use environment variables or command-line arguments to simplify mode selection.

4. **Real-World Transition Validation**:
    - Conduct trials with basic hardware setups and test against simulation results.

5. **Visualization Enhancements**:
    - Update `visualization.py` to reflect real hardware results and provide useful insights for monitoring.