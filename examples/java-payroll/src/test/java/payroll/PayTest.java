package payroll;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class PayTest {

    static final Employee ADA = new Employee("e1", "Ada", 2000);

    @Test
    void overtimeStartsPastFortyHours() {
        assertEquals(0, Pay.overtimeHours(new TimeSheet("e1", 12)));
        assertEquals(0, Pay.overtimeHours(new TimeSheet("e1", 40)));
        assertEquals(5, Pay.overtimeHours(new TimeSheet("e1", 45)));
    }

    @Test
    void grossPaysRegularHoursAtRate() {
        assertEquals(24_000, Pay.grossCents(ADA, new TimeSheet("e1", 12)));
    }

    @Test
    void grossPaysOvertimeAtTimeAndAHalf() {
        // 40h at $20.00 plus 5h at $30.00 = $800.00 + $150.00
        assertEquals(95_000, Pay.grossCents(ADA, new TimeSheet("e1", 45)));
    }
}
