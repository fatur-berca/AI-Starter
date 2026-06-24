### 2.4.3 System Configuration (One-Time Setup)

The **One-Time Setup (System Configuration)** page is a centralized, foundational administration interface within the **Master Lookup** menu in the Transportation Order Management (TOM) system. 

Rather than hardcoding business rules, email directories, layout properties, validation intervals, or system thresholds directly in the C# source code or SQL databases, developers utilize this module to store configuration mappings dynamically.

This design enables immediate system behavior modification without requiring application rebuilds, tests, or server re-deployments.

---

### **Why We Avoid Hardcoding (Dynamic Registry Advantages)**

1. **Zero Downtime Updates:** If an operational constant changes (such as the default import threshold, email ports, or API parameters), administrators modify the `Setup Value` via the UI. The application re-reads the value instantly without code compilation.
2. **Audit Trails & Security:** Modifications to the system configurations track audit logs (`UpdatedBy` and `UpdatedDate`) inside the database, whereas hotfixes to hardcoded code are harder to audit.
3. **Hierarchical Settings:** Using `Parent ID` and `Sort Order`, related configurations (e.g., mail server parameters) are cleanly grouped under a single parent node.

---

### **System Configuration List Table**

The main ledger grid displays all active and inactive configuration entries in the `APLOneTimeSetup` registry. This grid supports asynchronous server-side search, pagination, and multi-column filtering.

| **Column Name** | **Description** |
| --- | --- |
| **Status** | A green (`dot-on`) or red (`dot-off`) status dot indicating if the configuration key is currently active. Inactive configs are ignored by program lookups. |
| **Setup ID** | The unique, bolded alphanumeric key identifier (e.g. `DEFAULT_CURRENCY`, `FORECAST_MAX_WEEKS`) used by the C# codebase to fetch values. |
| **Description** | Summary detailing what system parameter or business logic this configuration controls. |
| **Setup Value** | The dynamic setting value string (e.g. `IDR`, `4`, `10.50`, `https://api.tom.com/`) read by the program. |
| **Parent ID** | An optional parent code representing hierarchical configuration groupings. |
| **Sort Order** | A numeric index determining the rendering sequence of child configuration nodes. |
| **Created By** | Username of the administrator who registered the config key. |
| **Created Date** | Ingestion timestamp formatted as `YYYY-MM-DD HH:MM`. |
| **Updated By** | Username of the planner who last updated the configuration value. |
| **Updated Date** | Timestamp of last modification formatted as `YYYY-MM-DD HH:MM`. |
| **Action** | Pencil icon button that launches the Add/Edit Modal loaded with the key's parameters. |

#### **Header Columns Filter**
Planners can perform precise searches on individual fields using the text input filters in the table sub-header:
* **Setup ID** (filters entries by matching the unique key)
* **Description** (filters entries by matching keyword)

---

### **Add / Edit One-Time Setup Modal**

Clicking the blue **Add New** button or the row action **Edit** pencil icon launches the sliding modal overlay form (`#mdSetup`).

#### **Input Fields & Specifications**

The modal form allows administrators to manage transport medium profiles using the following fields:

* **Setup ID (*):** A mandatory text input field. This is the alphanumeric constant used by the program to search the record (e.g., `FORECAST_MAX_WEEKS`). Limited to a maximum of **50 characters**.
* **Description:** An optional text description summarizing the purpose of the key (max **200 characters**).
* **Setup Value:** The actual string, integer, or decimal value used in calculations (max **500 characters**).
* **Parent ID:** An optional numerical field grouping related child items (e.g., grouping email SMTP records).
* **Sort Order:** A numerical sorting order index (defaults to `0`).
* **Status:** A dropdown select menu that controls the operational status (`Active` or `Inactive`).

---

### **Programmatic Retrieval Example (Technical Integration)**

Instead of hardcoding values inside C# code layers, developers fetch configurations dynamically.

#### **Traditional Hardcoding (BAD PRACTICE)**
```csharp
// High-risk: Changing this limit requires recompilation, unit tests, and server redeployment
int maxWeeks = 4; 
```

#### **TOM Dynamic Configuration (BEST PRACTICE)**
```csharp
// Safe: The limit is loaded at runtime from the system configuration registry
var limitConfig = _context.APLOneTimeSetup
    .FirstOrDefault(x => x.SetupId == "FORECAST_MAX_WEEKS" && x.IsActive);

int maxWeeks = limitConfig != null ? int.Parse(limitConfig.SetupValue) : 4;
```
