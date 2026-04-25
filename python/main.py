import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time
from scipy.signal import correlate2d

# ==============================
# Load image
# ==============================
img_gray = Image.open("image.png").convert("L")
image_uint8 = np.array(img_gray)
image = image_uint8.astype(np.float32) / 255.0

# ==============================
# Kernels
# ==============================
kernels = {
    "Vertical Edges": np.array([
        [1, 0, -1],
        [1, 0, -1],
        [1, 0, -1]
    ], dtype=np.float32),

    "Horizontal Edges": np.array([
        [1, 1, 1],
        [0, 0, 0],
        [-1, -1, -1]
    ], dtype=np.float32),

    "Sharpen": np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ], dtype=np.float32)
}

# ==============================
# Slow convolution (manual loops)
# ==============================
def slow_convolution(image, kernel):
    h, w = image.shape
    kh, kw = kernel.shape
    output = np.zeros((h - kh + 1, w - kw + 1), dtype=np.float32)

    for i in range(h - kh + 1):
        for j in range(w - kw + 1):
            region = image[i:i + kh, j:j + kw]
            output[i, j] = np.sum(region * kernel)

    return output

# ==============================
# Fast convolution (optimized)
# Using correlate2d so output matches slow method
# ==============================
def fast_convolution(image, kernel):
    return correlate2d(image, kernel, mode="valid")

# ==============================
# Run all kernels
# ==============================
slow_results = {}
fast_results = {}
slow_times = []
fast_times = []
kernel_names = []

for name, kernel in kernels.items():
    kernel_names.append(name)

    start = time.time()
    slow_out = slow_convolution(image, kernel)
    slow_time = time.time() - start

    start = time.time()
    fast_out = fast_convolution(image, kernel)
    fast_time = time.time() - start

    slow_results[name] = slow_out
    fast_results[name] = fast_out
    slow_times.append(slow_time)
    fast_times.append(fast_time)

    diff = np.sum(np.abs(slow_out - fast_out))

    print(f"\n{name}")
    print(f"Slow Time: {slow_time:.6f} sec")
    print(f"Fast Time: {fast_time:.6f} sec")
    print(f"Speedup: {slow_time / fast_time:.2f}x")
    print(f"Difference between outputs: {diff:.6f}")

# ==============================
# Show feature maps
# ==============================
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.title("Input Image")
plt.imshow(image, cmap="gray")
plt.axis("off")

plt.subplot(2, 2, 2)
plt.title("Vertical Edges")
plt.imshow(fast_results["Vertical Edges"], cmap="gray")
plt.axis("off")

plt.subplot(2, 2, 3)
plt.title("Horizontal Edges")
plt.imshow(fast_results["Horizontal Edges"], cmap="gray")
plt.axis("off")

plt.subplot(2, 2, 4)
plt.title("Sharpen")
plt.imshow(fast_results["Sharpen"], cmap="gray")
plt.axis("off")

plt.tight_layout()
plt.savefig("result.png", dpi=300, bbox_inches="tight")
plt.show()

# ==============================
# Performance graph
# ==============================
x = np.arange(len(kernel_names))
width = 0.35

plt.figure(figsize=(10, 5))
plt.bar(x - width / 2, slow_times, width, label="Slow (CPU)")
plt.bar(x + width / 2, fast_times, width, label="Fast (Accelerator)")
plt.title("Performance Comparison")
plt.ylabel("Execution Time (seconds)")
plt.xticks(x, kernel_names)
plt.legend()
plt.tight_layout()
plt.savefig("performance.png", dpi=300, bbox_inches="tight")
plt.show()

# ==============================
# Scalability test
# ==============================
sizes = [32, 64, 128, 256]
slow_scale = []
fast_scale = []

for s in sizes:
    resized_img = img_gray.resize((s, s))
    resized = np.array(resized_img).astype(np.float32) / 255.0
    kernel = kernels["Vertical Edges"]

    start = time.time()
    _ = slow_convolution(resized, kernel)
    slow_scale.append(time.time() - start)

    start = time.time()
    _ = fast_convolution(resized, kernel)
    fast_scale.append(time.time() - start)

plt.figure(figsize=(10, 5))
plt.plot(sizes, slow_scale, marker="o", label="Slow (CPU)")
plt.plot(sizes, fast_scale, marker="o", label="Fast (Accelerator)")
plt.title("Scalability Analysis")
plt.xlabel("Image Size")
plt.ylabel("Execution Time (seconds)")
plt.legend()
plt.tight_layout()
plt.savefig("scalability.png", dpi=300, bbox_inches="tight")
plt.show()