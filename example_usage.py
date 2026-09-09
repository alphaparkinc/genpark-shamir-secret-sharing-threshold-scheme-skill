"""Example usage for Shamir Secret Sharing Skill."""
from client import ShamirSecretSharing

def main():
    print("Executing Shamir Secret Sharing (k=3, n=5)...")
    sss = ShamirSecretSharing()
    secret_key = 987654321
    shares = sss.split_secret(secret_key, k=3, n=5)
    print("Generated 5 shares:")
    for s in shares:
        print(" ", s)

    # Reconstruct with any 3 shares
    recovered = sss.reconstruct_secret(shares[:3])
    print("Recovered secret:", recovered)
    assert recovered == secret_key, "Secret recovery failed"
    print("Shamir Secret Sharing verified successfully!")

if __name__ == "__main__":
    main()
