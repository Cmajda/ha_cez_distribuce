# Copilot Instructions (Repository)

## Commit messages

- Always write commit messages in English.
- Use Conventional Commits prefixes:
  feat:, fix:, docs:, style:, refactor:, perf:, test:, build:, ci:, chore:, revert:
- Use release/version commits as:
  chore(release): <version>
- Use dependency bumps as:
  build(deps): bump <package> to <version>

## Format

<type>(optional-scope): short imperative summary

## Examples

- feat(ui): add Docker version table sorting
- fix(api): handle null response from UniFi endpoint
- docs(readme): update local dev setup
- chore(release): 2.3.1
- build(deps): bump ruff to 0.14.0

---

## Project Overview

This repository contains the **ČEZ HDO integration** for Home Assistant. It fetches low/high tariff data from the ČEZ Distribuce API and provides entities and a Lovelace card for visualization.

### Key Components

- **Backend Integration**:
  - Located in `custom_components/cez_hdo/`.
  - Handles API communication, data processing, and Home Assistant entity creation.
  - Key files:
    - `coordinator.py`: Manages data fetching and updates.
    - `sensor.py` and `binary_sensor.py`: Define Home Assistant entities.
    - `config_flow.py`: Handles integration setup in the Home Assistant UI.

- **Frontend (Lovelace Card)**:
  - Source code in `dev/frontend/`.
  - Built using Node.js and bundled with Roll-up.
  - Key files:
    - `src/cez-hdo-card.ts`: Main Lovelace card implementation.
    - `src/cez-hdo-card-editor.ts`: Configuration editor for the card.

### Developer Workflows

#### Backend Development
- **Testing**: Use Home Assistant's development environment to test changes.
- **Diagnostics**: Add debug logs in `custom_components/cez_hdo/` files to troubleshoot issues.

#### Frontend Development
- **Install Dependencies**:
  ```bash
  cd dev/frontend
  npm install
  ```
- **Development Server**:
  ```bash
  npm run dev
  ```
- **Build for Production**:
  ```bash
  npm run build:prod
  ```
- **Deploy Built Files**:
  ```bash
  cd ../../dev
  ./deploy.sh
  ```

### Project-Specific Conventions

- **Translations**:
  - Translation files are located in `custom_components/cez_hdo/translations/`.
  - Use `cs.json` for Czech and `en.json` for English.

- **Documentation**:
  - User and developer guides are in `docs/`.
  - Separate folders for Czech (`cs/`) and English (`en/`).

- **Code Style**:
  - Follow Python conventions for backend code.
  - Use TypeScript conventions for frontend code.

### External Dependencies

- **Backend**:
  - Relies on Home Assistant's core libraries.

- **Frontend**:
  - Requires Node.js 18+ and npm/yarn.
  - Bundled with Roll-up.

### Integration Points

- **Home Assistant**:
  - The integration communicates with Home Assistant's entity registry and API.
  - Ensure compatibility with Home Assistant's latest version.

- **ČEZ Distribuce API**:
  - Fetches tariff data. Ensure API endpoints are up-to-date.

---

## Examples for AI Agents

- **Adding a New Sensor**:
  - Create a new file in `custom_components/cez_hdo/` (e.g., `new_sensor.py`).
  - Define the sensor class inheriting from `SensorEntity`.
  - Register the sensor in `__init__.py`.

- **Updating the Lovelace Card**:
  - Modify the TypeScript files in `dev/frontend/src/`.
  - Test changes using `npm run dev`.
  - Build and deploy using `npm run build:prod` and `./deploy.sh`.

- **Adding a Translation**:
  - Update `cs.json` and `en.json` in `custom_components/cez_hdo/translations/`.
  - Follow the existing key-value structure.

---

## Python Function Documentation

- Use the Google style format for documenting Python functions, as recommended in the [Home Assistant Development Guidelines](https://developers.home-assistant.io/docs/development_guidelines).

### Example:
```python
def example_function(param1: int, param2: str) -> bool:
    """
    Brief description of the function.

    Args:
        param1 (int): Description of the first parameter.
        param2 (str): Description of the second parameter.

    Returns:
        bool: Description of the return value.

    Raises:
        ValueError: Explanation of when this exception is raised.
    """
    # Function implementation
    pass
```

For further details, refer to the [README.md](../README.md) and documentation in `docs/`.
