package payroll;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class TaxTest {

    @ParameterizedTest
    @CsvSource({
        "0, 0",
        "30000, 3000",    // inside the 10% bracket
        "50000, 5000",    // first bracket edge
        "80000, 11000",   // 5000 + 30000 / 5
        "100000, 15000",  // second bracket edge
        "160000, 33000",  // 15000 + 60000 * 3 / 10
    })
    void withholdsProgressivelyByBracket(int grossCents, int taxCents) {
        assertEquals(taxCents, Tax.withholdingCents(grossCents));
    }

    @Test
    void netIsGrossMinusWithholding() {
        assertEquals(81_000, Tax.netCents(95_000));
    }
}
