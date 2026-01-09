import pygame
import random
import time
import sys
import json
import os
from datetime import datetime

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
FPS = 60
REACTION_THRESHOLD = 0.3  # seconds
ROUNDS_PER_PLAYER = 3
HIGH_SCORES_FILE = "high_scores.json"

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Reflex Shooter")
clock = pygame.time.Clock()

# Fonts
font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)
font_tiny = pygame.font.Font(None, 28)

# Generate simple sound effects
def generate_beep(frequency, duration):
    """Generate a simple beep sound"""
    try:
        import numpy as np
        sample_rate = 22050
        n_samples = int(round(duration * sample_rate))
        
        # Generate time array
        t = np.linspace(0, duration, n_samples, False)
        # Generate sine wave
        wave = np.sin(frequency * 2 * np.pi * t)
        # Scale to 16-bit range
        audio = (wave * 32767 * 0.3).astype(np.int16)
        # Make stereo
        stereo_audio = np.column_stack((audio, audio))
        
        sound = pygame.sndarray.make_sound(stereo_audio)
        return sound
    except Exception as e:
        print(f"Error generating beep: {e}")
        return None

def generate_explosion_sound():
    """Generate an explosion sound effect"""
    try:
        import numpy as np
        sample_rate = 22050
        duration = 0.3
        n_samples = int(round(duration * sample_rate))
        
        # Create noise that fades out
        noise = np.random.uniform(-1, 1, n_samples)
        # Apply fade-out envelope
        envelope = np.linspace(1, 0, n_samples)
        wave = noise * envelope
        
        # Scale to 16-bit range
        audio = (wave * 32767 * 0.5).astype(np.int16)
        # Make stereo
        stereo_audio = np.column_stack((audio, audio))
        
        sound = pygame.sndarray.make_sound(stereo_audio)
        return sound
    except Exception as e:
        print(f"Error generating explosion: {e}")
        return None

def generate_win_sound():
    """Generate a winning sound effect"""
    try:
        import numpy as np
        sample_rate = 22050
        duration = 0.5
        n_samples = int(round(duration * sample_rate))
        
        # Ascending notes: C, E, G
        frequencies = [523, 659, 784]
        samples_per_note = n_samples // len(frequencies)
        
        audio_parts = []
        for freq in frequencies:
            t = np.linspace(0, duration / len(frequencies), samples_per_note, False)
            wave = np.sin(freq * 2 * np.pi * t)
            audio_parts.append(wave)
        
        # Concatenate all notes
        full_wave = np.concatenate(audio_parts)
        # Scale to 16-bit range
        audio = (full_wave * 32767 * 0.3).astype(np.int16)
        # Make stereo
        stereo_audio = np.column_stack((audio, audio))
        
        sound = pygame.sndarray.make_sound(stereo_audio)
        return sound
    except Exception as e:
        print(f"Error generating win sound: {e}")
        return None

def generate_lose_sound():
    """Generate a losing sound effect"""
    try:
        import numpy as np
        sample_rate = 22050
        duration = 0.5
        n_samples = int(round(duration * sample_rate))
        
        # Descending notes: G, E, C
        frequencies = [392, 330, 262]
        samples_per_note = n_samples // len(frequencies)
        
        audio_parts = []
        for freq in frequencies:
            t = np.linspace(0, duration / len(frequencies), samples_per_note, False)
            wave = np.sin(freq * 2 * np.pi * t)
            audio_parts.append(wave)
        
        # Concatenate all notes
        full_wave = np.concatenate(audio_parts)
        # Scale to 16-bit range
        audio = (full_wave * 32767 * 0.3).astype(np.int16)
        # Make stereo
        stereo_audio = np.column_stack((audio, audio))
        
        sound = pygame.sndarray.make_sound(stereo_audio)
        return sound
    except Exception as e:
        print(f"Error generating lose sound: {e}")
        return None

# Initialize sounds
try:
    sound_countdown = generate_beep(800, 0.1)
    sound_shoot = generate_explosion_sound()
    sound_target = generate_beep(1200, 0.15)
    sound_win = generate_win_sound()
    sound_lose = generate_lose_sound()
    print("Sound effects loaded successfully!")
except Exception as e:
    print(f"Could not load sound effects: {e}")
    sound_countdown = None
    sound_shoot = None
    sound_target = None
    sound_win = None
    sound_lose = None

def get_player_names():
    """Get names for both players"""
    players = []
    
    for player_num in [1, 2]:
        name = ""
        input_active = True
        
        while input_active:
            screen.fill(BLACK)
            
            # Draw prompt
            prompt_text = font_medium.render(f"Enter Player {player_num} Name:", True, WHITE)
            prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(prompt_text, prompt_rect)
            
            # Draw input box
            input_text = font_small.render(name + "_", True, GREEN)
            input_rect = input_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            screen.blit(input_text, input_rect)
            
            # Instructions
            instruction_text = font_small.render("Press ENTER when done", True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
            screen.blit(instruction_text, instruction_rect)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(name) > 0:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key != pygame.K_RETURN and len(name) < 15:
                        name += event.unicode
        
        players.append(name)
    
    return players

def draw_shooter(x, y):
    """Draw the shooter at the bottom of the screen"""
    # Body (triangle)
    points = [(x, y - 30), (x - 20, y), (x + 20, y)]
    pygame.draw.polygon(screen, BLUE, points)
    # Gun barrel
    pygame.draw.rect(screen, BLUE, (x - 5, y - 50, 10, 20))

def draw_target(x, y):
    """Draw the target"""
    # Outer circle
    pygame.draw.circle(screen, RED, (x, y), 30)
    # Middle circle
    pygame.draw.circle(screen, WHITE, (x, y), 20)
    # Inner circle
    pygame.draw.circle(screen, RED, (x, y), 10)

def draw_explosion(x, y, frame):
    """Draw explosion animation"""
    max_frames = 20
    if frame >= max_frames:
        return False
    
    # Create expanding particles
    num_particles = 12
    max_radius = 80
    
    for i in range(num_particles):
        angle = (360 / num_particles) * i
        # Calculate particle position based on frame
        distance = (frame / max_frames) * max_radius
        particle_x = x + int(distance * pygame.math.Vector2(1, 0).rotate(angle).x)
        particle_y = y + int(distance * pygame.math.Vector2(1, 0).rotate(angle).y)
        
        # Particle size decreases over time
        particle_size = int(10 * (1 - frame / max_frames))
        if particle_size > 0:
            # Color fades from yellow to red to black
            if frame < max_frames / 2:
                color = YELLOW
            else:
                # Fade to red
                fade = (frame - max_frames / 2) / (max_frames / 2)
                color = (255, int(255 * (1 - fade)), 0)
            
            pygame.draw.circle(screen, color, (particle_x, particle_y), particle_size)
    
    # Draw central flash
    if frame < max_frames / 3:
        flash_size = int(40 * (1 - frame / (max_frames / 3)))
        pygame.draw.circle(screen, WHITE, (x, y), flash_size)
    
    return True

def show_result(won, reaction_time, player_name, round_num):
    """Show the result message"""
    screen.fill(BLACK)
    
    # Show player name and round
    player_text = font_medium.render(f"{player_name} - Round {round_num}", True, CYAN)
    player_rect = player_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(player_text, player_rect)
    
    if reaction_time == 0.0:
        # Premature shot
        result_text = font_large.render("TOO EARLY!", True, RED)
        result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(result_text, result_rect)
        
        message_text = font_medium.render("Wait for the target!", True, WHITE)
        message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(message_text, message_rect)
        
        # Play lose sound
        if sound_lose:
            sound_lose.play()
    else:
        if won:
            result_text = font_large.render("YOU WIN!", True, GREEN)
            # Play win sound
            if sound_win:
                sound_win.play()
        else:
            result_text = font_large.render("YOU ARE TOO SLOW!", True, RED)
            # Play lose sound
            if sound_lose:
                sound_lose.play()
        
        result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(result_text, result_rect)
        
        time_text = font_medium.render(f"Reaction Time: {reaction_time:.3f}s", True, WHITE)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(time_text, time_rect)
    
    instruction_text = font_small.render("Press SPACE to continue", True, WHITE)
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
    screen.blit(instruction_text, instruction_rect)
    
    pygame.display.flip()

def wait_for_space_or_esc():
    """Wait for space bar or escape key"""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False
        clock.tick(FPS)
    return False

def wait_for_space():
    """Wait only for space bar"""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
        clock.tick(FPS)
    return True

def play_game(player_name, round_num):
    """Main game loop"""
    shooter_x = SCREEN_WIDTH // 2
    shooter_y = SCREEN_HEIGHT - 40
    
    # Generate random target position
    target_x = random.randint(50, SCREEN_WIDTH - 50)
    target_y = random.randint(50, SCREEN_HEIGHT - 150)
    
    # Show player turn announcement
    screen.fill(BLACK)
    turn_text = font_large.render(f"{player_name}'s Turn", True, YELLOW)
    turn_rect = turn_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    screen.blit(turn_text, turn_rect)
    
    round_text = font_medium.render(f"Round {round_num}", True, WHITE)
    round_rect = round_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
    screen.blit(round_text, round_rect)
    
    pygame.display.flip()
    pygame.time.wait(2000)
    
    # Show countdown - check for early space press
    premature_shot = False
    for countdown in [3, 2, 1]:
        screen.fill(BLACK)
        countdown_text = font_large.render(str(countdown), True, YELLOW)
        countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(countdown_text, countdown_rect)
        pygame.display.flip()
        
        # Play countdown beep
        if sound_countdown:
            sound_countdown.play()
        
        # Check for events during countdown
        start_wait = time.time()
        while time.time() - start_wait < 1.0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    premature_shot = True
            clock.tick(FPS)
    
    # Clear screen and show "GET READY" - continue checking for early press
    screen.fill(BLACK)
    ready_text = font_large.render("GET READY!", True, YELLOW)
    ready_rect = ready_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(ready_text, ready_rect)
    pygame.display.flip()
    
    # Random delay with event checking
    delay_duration = random.randint(500, 2000) / 1000.0  # Convert to seconds
    start_wait = time.time()
    while time.time() - start_wait < delay_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                premature_shot = True
        clock.tick(FPS)
    
    # If premature shot detected, show immediate loss
    if premature_shot:
        show_result(False, 0.0, player_name, round_num)
        wait_for_space()
        return 999.0  # Return penalty time for early shot
    
    # Show target and start timing
    target_visible = True
    start_time = time.time()
    shot_fired = False
    reaction_time = 0
    
    # Play target appearance sound
    if sound_target:
        sound_target.play()
    
    # Explosion animation variables
    show_explosion_anim = False
    explosion_frame = 0
    explosion_x = target_x
    explosion_y = target_y
    
    while target_visible or show_explosion_anim:
        screen.fill(BLACK)
        
        # Draw shooter
        draw_shooter(shooter_x, shooter_y)
        
        # Draw target or explosion
        if target_visible:
            draw_target(target_x, target_y)
        elif show_explosion_anim:
            if not draw_explosion(explosion_x, explosion_y, explosion_frame):
                show_explosion_anim = False
            explosion_frame += 1
        
        # Draw player name and round
        name_text = font_small.render(f"Player: {player_name} - Round {round_num}", True, WHITE)
        screen.blit(name_text, (10, 10))
        
        # Draw instructions
        if target_visible:
            instruction_text = font_small.render("Press SPACE to shoot!", True, WHITE)
            screen.blit(instruction_text, (SCREEN_WIDTH - 320, 10))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not shot_fired and target_visible:
                    shot_fired = True
                    reaction_time = time.time() - start_time
                    target_visible = False
                    show_explosion_anim = True
                    explosion_frame = 0
                    # Play shoot sound
                    if sound_shoot:
                        sound_shoot.play()
        
        clock.tick(FPS)
    
    # Determine winner
    won = reaction_time < REACTION_THRESHOLD
    
    # Show result
    show_result(won, reaction_time, player_name, round_num)
    wait_for_space()
    
    return reaction_time

def load_high_scores():
    """Load high scores from file"""
    if os.path.exists(HIGH_SCORES_FILE):
        try:
            with open(HIGH_SCORES_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_high_scores(scores):
    """Save high scores to file"""
    try:
        with open(HIGH_SCORES_FILE, 'w') as f:
            json.dump(scores, f, indent=2)
    except:
        pass

def update_high_scores(player_name, best_time):
    """Update high scores with new entry"""
    scores = load_high_scores()
    
    # Add new score
    scores.append({
        'name': player_name,
        'time': best_time,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M')
    })
    
    # Sort by time (lower is better) and keep top 10
    scores = sorted(scores, key=lambda x: x['time'])[:10]
    
    save_high_scores(scores)
    return scores

def show_game_summary(player1_name, player1_times, player2_name, player2_times):
    """Show final game summary with all round times"""
    screen.fill(BLACK)
    
    # Title
    title_text = font_large.render("GAME SUMMARY", True, YELLOW)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(title_text, title_rect)
    
    # Player 1 stats
    y_offset = 130
    p1_title = font_medium.render(f"{player1_name}", True, CYAN)
    screen.blit(p1_title, (50, y_offset))
    y_offset += 50
    
    for i, time_val in enumerate(player1_times, 1):
        if time_val == 999.0:
            time_text = font_small.render(f"Round {i}: TOO EARLY", True, RED)
        else:
            color = GREEN if time_val < REACTION_THRESHOLD else RED
            time_text = font_small.render(f"Round {i}: {time_val:.3f}s", True, color)
        screen.blit(time_text, (70, y_offset))
        y_offset += 35
    
    # Player 1 best time
    valid_times_p1 = [t for t in player1_times if t != 999.0]
    best_p1 = min(valid_times_p1) if valid_times_p1 else 999.0
    best_text = font_small.render(f"Best: {best_p1:.3f}s" if best_p1 != 999.0 else "Best: N/A", True, WHITE)
    screen.blit(best_text, (70, y_offset))
    
    # Player 2 stats
    y_offset = 130
    p2_title = font_medium.render(f"{player2_name}", True, CYAN)
    screen.blit(p2_title, (SCREEN_WIDTH // 2 + 50, y_offset))
    y_offset += 50
    
    for i, time_val in enumerate(player2_times, 1):
        if time_val == 999.0:
            time_text = font_small.render(f"Round {i}: TOO EARLY", True, RED)
        else:
            color = GREEN if time_val < REACTION_THRESHOLD else RED
            time_text = font_small.render(f"Round {i}: {time_val:.3f}s", True, color)
        screen.blit(time_text, (SCREEN_WIDTH // 2 + 70, y_offset))
        y_offset += 35
    
    # Player 2 best time
    valid_times_p2 = [t for t in player2_times if t != 999.0]
    best_p2 = min(valid_times_p2) if valid_times_p2 else 999.0
    best_text = font_small.render(f"Best: {best_p2:.3f}s" if best_p2 != 999.0 else "Best: N/A", True, WHITE)
    screen.blit(best_text, (SCREEN_WIDTH // 2 + 70, y_offset))
    
    # Determine winner
    y_offset = 420
    if best_p1 < best_p2:
        winner_text = font_large.render(f"{player1_name} WINS!", True, GREEN)
    elif best_p2 < best_p1:
        winner_text = font_large.render(f"{player2_name} WINS!", True, GREEN)
    else:
        winner_text = font_large.render("IT'S A TIE!", True, YELLOW)
    
    winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
    screen.blit(winner_text, winner_rect)
    
    # Instructions
    instruction_text = font_small.render("Press SPACE to see high scores", True, WHITE)
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, 520))
    screen.blit(instruction_text, instruction_rect)
    
    pygame.display.flip()
    wait_for_space()
    
    return best_p1, best_p2

def show_high_scores():
    """Display high scores table"""
    scores = load_high_scores()
    
    screen.fill(BLACK)
    
    # Title
    title_text = font_large.render("HIGH SCORES", True, YELLOW)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(title_text, title_rect)
    
    # Column headers
    y_offset = 130
    rank_header = font_medium.render("Rank", True, WHITE)
    name_header = font_medium.render("Name", True, WHITE)
    time_header = font_medium.render("Time", True, WHITE)
    date_header = font_medium.render("Date", True, WHITE)
    
    screen.blit(rank_header, (50, y_offset))
    screen.blit(name_header, (150, y_offset))
    screen.blit(time_header, (400, y_offset))
    screen.blit(date_header, (550, y_offset))
    
    # Draw separator line
    pygame.draw.line(screen, WHITE, (40, y_offset + 40), (SCREEN_WIDTH - 40, y_offset + 40), 2)
    
    y_offset += 60
    
    # Display scores
    if scores:
        for i, score in enumerate(scores[:10], 1):
            color = CYAN if i <= 3 else WHITE
            rank_text = font_small.render(f"{i}", True, color)
            name_text = font_small.render(score['name'], True, color)
            time_text = font_small.render(f"{score['time']:.3f}s", True, color)
            date_text = font_tiny.render(score['date'], True, color)
            
            screen.blit(rank_text, (60, y_offset))
            screen.blit(name_text, (150, y_offset))
            screen.blit(time_text, (400, y_offset))
            screen.blit(date_text, (550, y_offset))
            
            y_offset += 35
    else:
        no_scores_text = font_medium.render("No high scores yet!", True, WHITE)
        no_scores_rect = no_scores_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset + 50))
        screen.blit(no_scores_text, no_scores_rect)
    
    # Instructions
    instruction_text = font_small.render("Press SPACE to play again or ESC to quit", True, WHITE)
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, 550))
    screen.blit(instruction_text, instruction_rect)
    
    pygame.display.flip()
    
    return wait_for_space_or_esc()

def main():
    """Main function"""
    playing = True
    
    while playing:
        # Get player names
        player1_name, player2_name = get_player_names()
        
        # Initialize score tracking
        player1_times = []
        player2_times = []
        
        # Play 6 rounds total (3 per player, alternating)
        for round_num in range(1, ROUNDS_PER_PLAYER + 1):
            # Player 1's turn
            reaction_time = play_game(player1_name, round_num)
            player1_times.append(reaction_time)
            
            # Player 2's turn
            reaction_time = play_game(player2_name, round_num)
            player2_times.append(reaction_time)
        
        # Show game summary
        best_p1, best_p2 = show_game_summary(player1_name, player1_times, player2_name, player2_times)
        
        # Update high scores for both players
        if best_p1 != 999.0:
            update_high_scores(player1_name, best_p1)
        if best_p2 != 999.0:
            update_high_scores(player2_name, best_p2)
        
        # Show high scores table
        playing = show_high_scores()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
