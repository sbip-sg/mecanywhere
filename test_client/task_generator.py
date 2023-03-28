import cloudpickle
import sys

if __name__ == "__main__":
    compute_file = sys.argv[1]

    # Read the function from a file
    with open(compute_file, "rb") as file:
        code = compile(file.read(), "addition.py", "exec")
        exec(code)

    # Save the function to a file using cloudpickle
    with open("function.pkl", "wb") as file:
        cloudpickle.dump(compute, file)

    # Load the function from the file using cloudpickle
    with open("function.pkl", "rb") as file:
        loaded_function = cloudpickle.load(file)

    # Make sure the loaded function is the same as the original function
    assert (
        loaded_function.__code__.co_code == compute.__code__.co_code
    ), "Functions are not the same"
