import java.time.Instant;

public class Main {

    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("Usage: java Main <subnet-cidr>");
            System.exit(1);
        }

        String cidr = args[0];

        try {
            ScanConfig config = ScanConfig.fromCidr(cidr);

            System.err.println("Scan started: " + Instant.now());

            ScannerEngine engine = new ScannerEngine(config);
            ScanReport report = engine.execute();

            System.err.println("Scan finished: " + Instant.now());

            String json = JsonSerializer.toJson(report);
            System.out.println(json);

        } catch (IllegalArgumentException e) {
            System.err.println("Configuration error: " + e.getMessage());
            System.exit(1);
        } catch (Exception e) {
            System.err.println("Fatal error: " + e.getMessage());
            System.exit(1);
        }
    }
}