from backend.mesa_model import PTSDModel

def test_model():
    print("Initializing Model...")
    try:
        model = PTSDModel(10, 10, "Private", 2, "High")
        print("Model Initialized Successfully.")
    except Exception as e:
        print(f"FAILED to initialize model: {e}")
        return

    print("Running Steps...")
    try:
        for i in range(5):
            model.step()
            print(f"Step {i+1}: Soldier Stress={model.soldier.stress} Pos={model.soldier.pos}")
        print("Simulation Run Successfully.")
    except Exception as e:
        print(f"FAILED during simulation step: {e}")

if __name__ == "__main__":
    test_model()
