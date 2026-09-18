import re

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    content = f.read()

old_add_fee = """    fun addOrUpdateFee(fee: Fee) {
        viewModelScope.launch {
            repository.addFee(fee)
        }
    }"""

new_add_fee = """    fun addOrUpdateFee(fee: Fee) {
        viewModelScope.launch {
            val role = repository.currentUserFlow.value?.role?.uppercase()?.trim() ?: ""
            if (role != "PRINCIPAL" && role != "HEAD_ADMIN" && role != "ADMIN") {
                _toastMessage.value = "Unauthorized: Only management can modify fees."
                return@launch
            }
            repository.addFee(fee)
        }
    }"""

content = content.replace(old_add_fee, new_add_fee)

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.write(content)
