import java.net.InetAddress;
import java.net.UnknownHostException;

public class ScanConfig {

    public final InetAddress networkAddress;
    public final int prefixLength;
    public final int startPort = 1;
    public final int endPort = 1000;
    public final int connectTimeoutMs = 800;
    public final int readTimeoutMs = 300;
    public final int rateLimitPerSecond = 400;

    private ScanConfig(InetAddress networkAddress, int prefixLength) {
        this.networkAddress = networkAddress;
        this.prefixLength = prefixLength;
    }

    public static ScanConfig fromCidr(String cidr) {
        try {
            String[] parts = cidr.split("/");
            if (parts.length != 2) {
                throw new IllegalArgumentException("Invalid CIDR format");
            }

            InetAddress addr = InetAddress.getByName(parts[0]);
            int prefix = Integer.parseInt(parts[1]);

            if (prefix < 16) {
                throw new IllegalArgumentException("Subnet larger than /16 not allowed");
            }

            if (prefix > 32) {
                throw new IllegalArgumentException("Invalid prefix length");
            }

            return new ScanConfig(addr, prefix);

        } catch (UnknownHostException e) {
            throw new IllegalArgumentException("Invalid IP address");
        }
    }
}