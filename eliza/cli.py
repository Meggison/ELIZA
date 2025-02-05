"""
Command-line interface for the ELIZA chatbot.
"""

import argparse
import sys
from .core.chatbot import Eliza

def main():
    """
    Main entry point for the CLI application.
    """
    parser = argparse.ArgumentParser(description='ELIZA Chatbot CLI')
    parser.add_argument('--session-file', 
                       default='eliza_session.json',
                       help='Path to save session history')
    parser.add_argument('--debug', 
                       action='store_true',
                       help='Enable debug output')
    
    args = parser.parse_args()
    
    # Initialize ELIZA
    eliza = Eliza()
    print("ELIZA: Hello! I'm here to listen and support you. How are you feeling today?")
    
    try:
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("ELIZA: Thank you for sharing with me today. Take care of yourself.")
                    eliza.save_session(args.session_file)
                    break
                    
                response = eliza.respond(user_input)
                print(f"ELIZA: {response}")
                
            except (KeyboardInterrupt, EOFError):
                print("\nELIZA: I understand you need to go. Take care!")
                eliza.save_session(args.session_file)
                break
                
    except Exception as e:
        if args.debug:
            print(f"Error: {e}", file=sys.stderr)
        else:
            print("An error occurred. Please try again.", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
