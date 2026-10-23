# Week 1 CS Core: DBMS ACID & Normalization

## 1. ACID Properties (Banking Transfer)
- **Atomicity:** All or nothing. If a debit succeeds but the credit fails, rollback the debit.
- **Consistency:** Valid state → Valid state. Money cannot vanish; total balances remain constant.
- **Isolation:** Concurrent transactions don't interfere. Intermediate states are hidden.
- **Durability:** Once committed, changes survive a power outage (written to disk).

## 2. Normalization (1NF → 3NF)
- **1NF:** Atomic values only (no lists/arrays in a cell).
- **2NF:** 1NF + No partial dependencies. (e.g., `StudentName` should not depend only on `StudentID` if the PK is `(StudentID, CourseID)`).
- **3NF:** 2NF + No transitive dependencies. (e.g., `City` depends on `ZipCode`, which depends on `StudentID`. Split into a `ZipCodes` table).

## 3. Practice Questions
**Q1: What violates 2NF?**
A table `(OrderID, ProductID, ProductName, Quantity)` where `ProductName` depends only on `ProductID` (part of the composite key). Fix: Split into `OrderDetails(OrderID, ProductID, Quantity)` and `Products(ProductID, ProductName)`.

**Q2: Why is 3NF enough for OLTP?**
3NF eliminates most update anomalies while keeping JOINs manageable. BCNF and higher normal forms overcomplicate queries for rare edge cases.

## 4. Denormalization
- **When:** Read-heavy workloads (dashboards, analytics) where JOINs are too slow.
- **Trade-off:** Faster reads vs. slower writes and risk of data inconsistency.

## 5. SQL Practice
- Wrote a complete SQLite script (`cs_core/wk1_normalization.sql`) demonstrating the 1NF → 2NF → 3NF decomposition of a bookstore database.
