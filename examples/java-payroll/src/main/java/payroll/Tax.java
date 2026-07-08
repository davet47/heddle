package payroll;

/**
 * Progressive weekly withholding over integer cents: 10% to $500.00, 20% to
 * $1,000.00, 30% above — floored per bracket, so more gross never withholds less.
 */
public final class Tax {

    static final int BRACKET_1_TOP_CENTS = 50_000;
    static final int BRACKET_2_TOP_CENTS = 100_000;

    private Tax() {}

    public static int withholdingCents(int grossCents) {
        int tax = Math.min(grossCents, BRACKET_1_TOP_CENTS) / 10;
        if (grossCents > BRACKET_1_TOP_CENTS) {
            tax += (Math.min(grossCents, BRACKET_2_TOP_CENTS) - BRACKET_1_TOP_CENTS) / 5;
        }
        if (grossCents > BRACKET_2_TOP_CENTS) {
            tax += (grossCents - BRACKET_2_TOP_CENTS) * 3 / 10;
        }
        return tax;
    }

    /** Exactly gross minus withholding — the identity payslips must reproduce. */
    public static int netCents(int grossCents) {
        return grossCents - withholdingCents(grossCents);
    }
}
