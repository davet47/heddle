package payroll;

import java.util.List;

import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class PayrollTest {

    static final Employee ADA = new Employee("e1", "Ada", 2000);
    static final TimeSheet WEEK = new TimeSheet("e1", 45);

    @Test
    void slipRunsTheWholePipeline() {
        assertEquals(new PaySlip("e1", 95_000, 14_000, 81_000), Payroll.slipFor(ADA, WEEK));
    }

    @Test
    void totalNetSumsEverySlip() {
        PaySlip a = new PaySlip("e1", 95_000, 14_000, 81_000);
        PaySlip b = new PaySlip("e2", 24_000, 2_400, 21_600);
        assertEquals(102_600, Payroll.totalNetCents(List.of(a, b)));
        assertEquals(0, Payroll.totalNetCents(List.of()));
    }

    @Nested
    class Rendering {

        @Test
        void formatsCentsAsDollars() {
            assertEquals("$950.00", Payroll.formatCents(95_000));
            assertEquals("$0.05", Payroll.formatCents(5));
            assertEquals("-$12.34", Payroll.formatCents(-1234));
        }

        @Test
        void rendersOneLinePerField() {
            String s = Payroll.render(ADA, Payroll.slipFor(ADA, WEEK));
            assertTrue(s.startsWith("Ada (e1)"));
            assertTrue(s.contains("gross $950.00"));
            assertTrue(s.endsWith("net   $810.00"));
        }
    }
}
