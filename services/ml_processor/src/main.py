import time


def main():
    print("Hello from social-worker!")
    print("Simulating a worker... Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("Worker shutting down gracefully")


if __name__ == "__main__":
    main()
