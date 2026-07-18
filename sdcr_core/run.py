from sdcr_core.core.gksl_locked_qubit import run_locked_qubit_benchmark
from sdcr_core.io.outputs import write_all_outputs

def main():
    result = run_locked_qubit_benchmark(eta_sym=1.0)
    write_all_outputs(result)

if __name__ == "__main__":
    main()
