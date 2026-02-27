import java.util.Map;

public class ServiceMapper {

    private static final Map<Integer, String> PORT_MAP = Map.of(
            22, "ssh",
            80, "http",
            443, "https",
            21, "ftp",
            25, "smtp",
            3306, "mysql",
            5432, "postgres",
            6379, "redis",
            8080, "http-alt"
    );

    public static String map(int port) {
        return PORT_MAP.getOrDefault(port, "unknown");
    }
}