# ✨ DYNAMIC FORM PARAMETERS - User-Friendly Input!

## 🎯 What Changed

**Before:** JSON textarea for parameters (difficult, error-prone)
```json
{
  "title": "",
  "message": "",
  "urgent": false
}
```

**After:** Smart dynamic form fields based on parameter types!
- **String** → Text input
- **Number** → Number input
- **Boolean** → Radio buttons (True/False)
- **Password** → Password input (hidden)
- **Required fields** → Automatic validation

---

## 🚀 How It Works

### Step 1: Select Integration & Task
1. Select integration (e.g., "Teams")
2. Select task (e.g., "Send Notification")

### Step 2: Dynamic Form Appears!

```
┌─────────────────────────────────────────┐
│ Task Parameters                         │
├─────────────────────────────────────────┤
│ Message Title * (string)                │
│ [Enter title___________________]        │
│ The title of the notification           │
│                                         │
│ Message Content * (string)              │
│ [Enter message_________________]        │
│ The main message content                │
│                                         │
│ Is Urgent (boolean)                     │
│ ○ True  ● False                         │
│ Mark as urgent notification             │
│                                         │
│ Priority Level (number)                 │
│ [1_____]                                │
│ Priority from 1-5                       │
└─────────────────────────────────────────┘
```

---

## ✅ Features

### 1. **Type-Specific Inputs**
- **String**: Regular text box
- **Number**: Number input with validation
- **Boolean**: Radio buttons (True/False)
- **Password**: Masked input

### 2. **Required Field Validation**
- Red asterisk (*) for required fields
- Browser validation on submit
- Clear visual indicators

### 3. **Help Text**
- Parameter description shown below each field
- Type indicator next to label
- Contextual hints

### 4. **Toggle Between Form & JSON**
- Button: "{ } Show JSON" / "📝 Show Form"
- Switch to JSON for advanced use
- Switch to Form for easy use

### 5. **Fallback for No Parameters**
- If integration type has no tasks → Manual JSON input
- If task has no parameters → Clean interface

---

## 📋 Example Scenarios

### Scenario 1: Send Teams Notification

**Task**: Send Notification

**Parameters Defined:**
- `title` (string, required)
- `message` (string, required)
- `urgent` (boolean, optional)

**Form Shows:**
```
Title * (string)
[_________________]

Message * (string)
[_________________]

Urgent (boolean)
○ True  ● False
```

**Result:** Clean, user-friendly form!

---

### Scenario 2: Create Jira Issue

**Task**: Create Issue

**Parameters:**
- `project` (string, required)
- `summary` (string, required)
- `description` (string, optional)
- `priority` (number, optional)

**Form Shows:**
```
Project * (string)
[Enter project key__]
The Jira project key

Summary * (string)
[Enter summary_____]
Brief issue summary

Description (string)
[Enter description_]
Detailed description

Priority (number)
[1]
Priority level 1-5
```

---

### Scenario 3: API Call with Auth

**Task**: Make API Call

**Parameters:**
- `url` (string, required)
- `api_key` (password, required)
- `timeout` (number, optional)

**Form Shows:**
```
URL * (string)
[Enter URL________]

API Key * (password)
[••••••••••••••••]
Your API key (hidden)

Timeout (number)
[30]
Timeout in seconds
```

---

## 🎨 Visual Design

### Input Styling:
- Clean, modern text inputs
- Blue focus ring on active field
- Gray background for form container
- Proper spacing and padding

### Required Fields:
- Red asterisk (*) next to label
- Browser validation on submit
- Clear error messages

### Type Indicators:
- Small gray text showing type: `(string)`, `(number)`, etc.
- Helps users understand expected input

### Help Text:
- Small gray text below input
- Shows parameter description
- Contextual guidance

---

## 🔄 Toggle View

### Form View (Default):
- User-friendly inputs
- Type-appropriate controls
- Validation built-in
- No JSON knowledge needed

### JSON View:
- For power users
- Advanced configuration
- Complex data structures
- Manual editing

**Toggle Button:**
```
[📝 Show Form] ⟷ [{ } Show JSON]
```

---

## ✨ Benefits

### For Regular Users:
- ✅ No JSON knowledge needed
- ✅ Clear field labels
- ✅ Type-safe inputs
- ✅ Built-in validation
- ✅ Help text for each field

### For Power Users:
- ✅ Can switch to JSON view
- ✅ Advanced editing available
- ✅ Complex structures supported

### For Everyone:
- ✅ Fewer errors
- ✅ Faster workflow creation
- ✅ Better user experience
- ✅ Professional interface

---

## 🚀 Quick Start

1. **Restart Frontend:**
   ```bash
   docker-compose restart frontend
   ```

2. **Create Workflow:**
   - Go to Workflows
   - Create or edit workflow
   - Click "Add Node"

3. **See Dynamic Form:**
   - Select integration
   - Select task
   - **Dynamic form appears!**
   - Fill in fields easily
   - Submit!

---

## 🎯 Example Usage

### Before (JSON):
```
User must type:
{
  "title": "System Alert",
  "message": "Server is down",
  "urgent": true,
  "priority": 5
}
```
❌ Error-prone
❌ Requires JSON knowledge
❌ Easy to make syntax mistakes

### After (Form):
```
Title: [System Alert_______]
Message: [Server is down___]
Urgent: ● True  ○ False
Priority: [5]
```
✅ Easy to use
✅ No JSON needed
✅ Validation built-in

---

## 📝 Creating Integration Types with Good Parameters

When creating integration types, define parameters with:

1. **Clear Names**: `message_title` not `mt`
2. **Good Descriptions**: "The title shown at top of notification"
3. **Correct Types**: string, number, boolean, password
4. **Required Flag**: Mark what's mandatory

Example:
```javascript
{
  name: "title",
  type: "string",
  required: true,
  description: "The title of the notification"
}
```

This creates:
```
Title * (string)
[_________________]
The title of the notification
```

---

## 🎉 Summary

### Old Way:
- Type JSON manually
- Easy syntax errors
- Need JSON knowledge
- Time-consuming

### New Way:
- Fill in form fields
- Type-safe inputs
- No JSON needed
- Fast and easy!

---

**Just restart frontend and enjoy the new dynamic forms!** ✨

```bash
docker-compose restart frontend
```

See it in action:
1. Workflows → Add Node
2. Select integration with tasks
3. **Dynamic form appears!**
4. Fill fields → Add Node → Done! 🎉
