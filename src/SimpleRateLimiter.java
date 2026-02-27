import java.util.concurrent.Semaphore;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class SimpleRateLimiter {

    private final Semaphore semaphore;

    public SimpleRateLimiter(int permitsPerSecond) {
        this.semaphore = new Semaphore(permitsPerSecond);

        Executors.newSingleThreadScheduledExecutor()
                .scheduleAtFixedRate(() -> {
                    int deficit = permitsPerSecond - semaphore.availablePermits();
                    if (deficit > 0) {
                        semaphore.release(deficit);
                    }
                }, 1, 1, TimeUnit.SECONDS);
    }

    public void acquire() {
        try {
            semaphore.acquire();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}