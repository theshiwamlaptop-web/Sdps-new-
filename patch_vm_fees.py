import re

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    content = f.read()

old_add_fee = """    fun addOrUpdateFee(fee: Fee) {
        viewModelScope.launch {
            repository.addOrUpdateFee(fee)
        }
    }"""

new_add_fee = """    fun addOrUpdateFee(fee: Fee) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN" && role != "ADMIN") {
                _toastMessage.value = "Unauthorized: Only management can modify fees."
                return@launch
            }
            repository.addOrUpdateFee(fee)
        }
    }"""

content = content.replace(old_add_fee, new_add_fee)

old_delete_fee = """    fun deleteFee(feeId: String) {
        viewModelScope.launch {
            repository.deleteFee(feeId)
        }
    }"""

new_delete_fee = """    fun deleteFee(feeId: String) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN" && role != "ADMIN") {
                _toastMessage.value = "Unauthorized: Only management can delete fees."
                return@launch
            }
            repository.deleteFee(feeId)
        }
    }"""

content = content.replace(old_delete_fee, new_delete_fee)


old_add_payroll = """    fun addOrUpdatePayroll(payroll: Payroll) {
        viewModelScope.launch {
            repository.addOrUpdatePayroll(payroll)
        }
    }"""

new_add_payroll = """    fun addOrUpdatePayroll(payroll: Payroll) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN") {
                _toastMessage.value = "Unauthorized: Only Principal/Head Admin can modify payroll."
                return@launch
            }
            repository.addOrUpdatePayroll(payroll)
        }
    }"""

content = content.replace(old_add_payroll, new_add_payroll)

old_delete_payroll = """    fun deletePayrollsByTeacher(teacherId: String) {
        viewModelScope.launch {
            repository.deletePayrollsByTeacher(teacherId)
        }
    }"""

new_delete_payroll = """    fun deletePayrollsByTeacher(teacherId: String) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN") {
                _toastMessage.value = "Unauthorized: Only Principal/Head Admin can delete payrolls."
                return@launch
            }
            repository.deletePayrollsByTeacher(teacherId)
        }
    }"""

content = content.replace(old_delete_payroll, new_delete_payroll)


with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.write(content)
