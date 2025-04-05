#ifndef ADCTEMPLATE_H_!(GUID)
#define ADCTEMPLATE_H_!(GUID)

#include <string>
#include <list>

namespace ADC
{
    /// <summary>
    /// !(COMMAND_DESCRIPTION)
    /// </summary>
    class !(COMMAND_NAME)
    {
	public:

        !(COMMAND_NAME)();

		virtual ~!(COMMAND_NAME)();

	public:

        #pragma region Enums
        /// START FOR EACH ENUMTYPE
        /// <summary>
        /// !(ENUM_DESCRIPTION)
        /// </summary>
        enum !(ENUM_NAME)
        {
            /// <summary>
            /// Basic holder for unknown values
            /// </summary>
            Unknown = 0,

            /// START FOR EACH ENUM_VALUE
            /// <summary>
            /// !(ENUM_VALUE_DESCRIPTION)
            /// </summary>
            !(ENUM_VALUE_NAME) = !(ENUM_VALUE_VALUE)
            /// END FOR EACH ENUM_VALUE
        };
        /// END FOR EACH ENUMTYPE
        #pragma endregion

        #pragma region Positional parameters

        /// START FOR EACH POSITIONAL_PARAMETER
        /// <summary>
        /// !(PARAMETER_DESCRIPTION)
        /// </summary>
        !(PARAMETER_TYPE) Get!(PARAMETER_NAME)() const;

		Set!(PARAMETER_NAME)(!(PARAMETER_TYPE) value);
        /// END FOR EACH POSITIONAL_PARAMETER

        #pragma endregion

        #pragma region Named parameters

        /// START FOR EACH NAMED_PARAMETER
        /// <summary>
        /// !(PARAMETER_DESCRIPTION)
        /// </summary>
        !(PARAMETER_TYPE) Get!(PARAMETER_NAME) const;

		Set!(PARAMETER_NAME)(!(PARAMETER_TYPE) value);
        /// END FOR EACH NAMED_PARAMETER

        #pragma endregion

        #pragma region Methods

        /// START FOR EACH PARAMETER_LIST
        /// <summary>
        /// 
        /// </summary>
		std::string Get!(PARAMETER_NAME)Value() const;
        /// END FOR EACH PARAMETER_LIST

        #pragma endregion

        /// <summary>
        /// 
        /// </summary>
		std::string ConstructMessage();

	private:

		const std::string COMMAND_NAME = "!(COMMAND_ID)";
        const std::string SEPARATOR = " ";

		#pragma region Parameters
		/// START FOR EACH PARAMETER_LIST
        /// <summary>
        /// 
        /// </summary>
		!(PARAMETER_TYPE) m_!(PARAMETER_NAME);
		/// END FOR EACH PARAMETER_LIST
		#pragma endregion
    };
}

#endif // ADCTEMPLATE_H_!(GUID)