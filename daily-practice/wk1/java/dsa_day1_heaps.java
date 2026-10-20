import java.util.*;

public class dsa_day1_heaps {
    public static void main(String[] args) {
        System.out.println("=== 1. BASIC MIN-HEAP ===");
        PriorityQueue<Integer> minHeap = new PriorityQueue<>();
        minHeap.add(5); minHeap.add(2); minHeap.add(8); minHeap.add(1);
        System.out.println("peek: " + minHeap.peek());
        System.out.println("poll: " + minHeap.poll());
        System.out.println("after poll: " + minHeap);

        System.out.println("\n=== 2. MAX-HEAP ===");
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        maxHeap.add(5); maxHeap.add(2); maxHeap.add(8);
        System.out.println("peek: " + maxHeap.peek());

        System.out.println("\n=== 3. TOP-K (Size-K Min-Heap) ===");
        int[] nums = {3, 1, 5, 12, 2, 11, 7};
        int k = 3;
        PriorityQueue<Integer> topK = new PriorityQueue<>();
        for (int num : nums) {
            topK.add(num);
            if (topK.size() > k) topK.poll();
        }
        System.out.println("Top " + k + ": " + topK);

        System.out.println("\n=== 4. HEAP SORT ===");
        int[] arr = {4, 10, 3, 5, 1};
        PriorityQueue<Integer> heapSort = new PriorityQueue<>();
        for (int num : arr) {
            heapSort.add(num);
        }
        for (int i = 0; i < arr.length; i++) {
            arr[i] = heapSort.poll();
        }
        System.out.println("Sorted array: " + Arrays.toString(arr));        

    }
}
