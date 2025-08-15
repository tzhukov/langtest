#!/usr/bin/env python3
"""Run the Autonomous Updater Agent to implement new features."""

import sys
import os
import argparse

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from langest.agents.autonomous_updater import AutonomousUpdaterAgent


def main():
    """Main function to run the autonomous updater."""
    parser = argparse.ArgumentParser(description="""
    Run the Autonomous Updater Agent to implement new features in a codebase.
    The agent reads a requirements file, analyzes the project, and iteratively
    applies changes until the project's tests pass.
    """)
    
    parser.add_argument(
        "requirements_file",
        type=str,
        help="Path to the text file containing the new requirements."
    )
    
    parser.add_argument(
        "--project-path",
        type=str,
        default=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'generated_fullstack_service')),
        help="Path to the project directory to be updated. Defaults to the generated_fullstack_service directory."
    )

    parser.add_argument(
        "--test-command",
        type=str,
        default="make test",
        help="The command to run to verify the changes. Defaults to 'make test'."
    )

    args = parser.parse_args()

    # Check if .env file exists
    env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
    if not os.path.exists(env_file):
        print("⚠️  WARNING: .env file not found!")
        print("   The updater agent needs your GROQ_API_KEY to function.")
        print("   Please copy .env.example to .env and add your API key.")
        sys.exit(1)

    try:
        agent = AutonomousUpdaterAgent()
        success = agent.run_update(
            project_path=args.project_path,
            requirements_path=args.requirements_file,
            verification_command=args.test_command
        )

        if success:
            print("\n✅ Autonomous update completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Autonomous update failed.")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()