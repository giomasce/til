## Obtain a stacktrace when throwing an exception in C++

You can use the following code in a header. You also have to declare
`bool mmpp_abort` somewhere in the code. Some headers are probably
excessive. It uses GCC-specific interfaces.

If it does not work (in particular, if it cannot resolve symbols),
check that `-g` is on and possibly also add `-rdynamic` or
`-export-dynamic` to the linker.

References:

 * https://gist.github.com/fmela/591333

 * https://stupefydeveloper.blogspot.it/2008/10/cc-call-stack.html

 * http://stackoverflow.com/q/11731229/807307


```cpp
#ifdef __GNUG__
#include <set>
#include <string>
#include <vector>
#include <sstream>
#include <ostream>
#include <iostream>
#include <execinfo.h>
#include <cxxabi.h>
#include <dlfcn.h>
#include <stdlib.h>

// Taken from https://stupefydeveloper.blogspot.it/2008/10/cc-call-stack.html and partially adapted
inline static std::vector< std::string > dump_stacktrace(size_t depth) {
    using namespace std;
    using namespace abi;

    vector< string > ret;
    vector< void* > trace(depth);
    Dl_info dlinfo;
    int status;
    const char *symname;
    char *demangled;
    int trace_size = backtrace(trace.data(), depth);
    for (int i=0; i<trace_size; ++i)
    {
        if(!dladdr(trace[i], &dlinfo))
            continue;

        symname = dlinfo.dli_sname;

        demangled = __cxa_demangle(symname, NULL, 0, &status);
        if(status == 0 && demangled)
            symname = demangled;

        ostringstream oss;
        oss << "address: 0x" << trace[i] << ", object: " << dlinfo.dli_fname << ", function: " << symname;
        ret.push_back(oss.str());

        if (demangled)
            free(demangled);
    }
    return ret;
}

inline static std::vector< std::string > dump_stacktrace() {
    for (size_t depth = 10; ; depth *= 2) {
        auto ret = dump_stacktrace(depth);
        if (ret.size() < depth) {
            return ret;
        }
    }
}

#else
inline static std::vector< std::string > dump_stacktrace(int depth=0) {
    return {};
}
#endif

extern bool mmpp_abort;

class MMPPException {
public:
    MMPPException(std::string reason) : reason(reason), stacktrace(dump_stacktrace()) {
        if (mmpp_abort) {
            this->print_stacktrace(std::cerr);
            abort();
        }
    }
    const std::string &get_reason() const {
        return this->reason;
    }
    const std::vector< std::string > &get_stacktrace() const {
        return this->stacktrace;
    }
    void print_stacktrace(std::ostream &st) const {
        using namespace std;
        st << "Stack trace:" << endl;
        for (auto &frame : this->stacktrace) {
            st << "  * " << frame << endl;
        }
        st << "End of stack trace" << endl;
        st.flush();
    }

private:
    std::string reason;
    std::vector< std::string > stacktrace;
};

inline static void assert_or_throw(bool cond, std::string reason="") {
    if (!cond) {
        throw MMPPException(reason);
    }
}
```
