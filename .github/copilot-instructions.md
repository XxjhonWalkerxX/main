<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Tutor Plugin for Custom Registration Fields

This is a Tutor plugin project for Open edX that adds custom registration fields to the authentication system.

## Context
- This plugin extends Open edX registration to include Mexican-specific fields
- Fields include: primer_apellido, segundo_apellido, numero_telefono, estado, municipio, nombre_escuela, cct, grado, curp
- Works with a custom MFE (frontend-app-authn fork) that sends these fields
- Uses Django models and migrations to store the additional user data

## Key Components
- Plugin configuration and patches for Open edX
- Django models to store custom field data
- Database migrations for the new fields
- Integration with Tutor's plugin system

## Development Guidelines
- Follow Tutor plugin best practices
- Ensure compatibility with Open edX Sumac (19.0.0)
- Use proper Django model relationships and validations
- Include proper error handling for field validation
